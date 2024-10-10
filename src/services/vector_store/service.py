
import os
import time
import datetime
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from dotenv import load_dotenv

from helpers import get_llm
from services.zapi import WhatsAppMessage
from helpers.tracer import TracerFactory
from helpers.logger import logger

load_dotenv()

tracer = TracerFactory.get_tracer()
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))


class VectorStoreWrapper:
    def __init__(self, index_name: str):
        self.index = self.__get_or_create_index(index_name)
        self.embeddings = get_llm("openai", "text-embedding-3-large")
        self.vector_store = PineconeVectorStore(index=self.index,
                                                embedding=self.embeddings)

    def __get_or_create_index(self, index_name: str):
        existing_indexes = [index_info["name"]
                            for index_info in pc.list_indexes()]

        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=3072,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            while not pc.describe_index(index_name).status["ready"]:
                time.sleep(1)

        return pc.Index(index_name)

    def __render_document(self, message: WhatsAppMessage) -> Document:
        date = datetime.datetime.fromtimestamp(message.momment / 1000).\
            strftime("%Y-%m-%d %H:%M:%S")
        chatName = f" [chat:{message.chatName}]" \
            if message.chatName else ""
        replyTo = f" [replyTo:#{message.referenceMessageId}]" \
            if message.referenceMessageId else ""
        textMessageExtras = ""
        if message.text.title:
            textMessageExtras += f"\n\t{message.text.title}"
        if message.text.description:
            textMessageExtras += f"\n\t{message.text.description}"
        if message.text.url:
            textMessageExtras += f"\n\t{message.text.url}"

        return Document(
            page_content=f"#{message.messageId} [{date}]{chatName}{replyTo} "
                         f"{message.senderName}: "
                         f"{message.text.message}{textMessageExtras}",
            metadata=message.model_dump(exclude_none=True))

    # TODO: Improve session identification
    #   - reply identification
    #   - semantic proximity
    #   - avoid using timestamp
    def __get_session_id(self, message: WhatsAppMessage):
        date_with_hour = datetime.datetime\
            .fromtimestamp(message.momment / 1000)\
            .strftime("%Y-%m-%d-%H")
        return f"{message.connectedPhone}-{message.chatName}-{date_with_hour}"

    def add_message(self, message: WhatsAppMessage):
        tracer.init(session_id=self.__get_session_id(message))
        document = self.__render_document(message)
        logger.debug(f"Adding document to vector store: {document}")
        self.vector_store.add_documents(documents=[document],
                                        ids=[document.metadata['messageId']],
                                        namespace=message.connectedPhone)
        tracer.end()

    def search(self, namespace, filter, backoff_jump=1000):
        k_size = backoff_jump
        results = []
        while True:
            results = self.vector_store.similarity_search(
                "",  # Dummy string - we want to search all
                namespace=namespace,
                k=k_size,
                filter=filter
            )
            if len(results) < k_size:
                break
            k_size += backoff_jump
        return results


class VectorStoreFactory:
    vector_store_instances = {}

    @staticmethod
    def get_vector_store(index_name: str) -> VectorStoreWrapper:
        if index_name not in VectorStoreFactory.vector_store_instances:
            VectorStoreFactory.vector_store_instances[index_name] = \
                VectorStoreWrapper(index_name)
        return VectorStoreFactory.vector_store_instances[index_name]
