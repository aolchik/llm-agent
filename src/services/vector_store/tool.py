import datetime

from crewai_tools import BaseTool
from typing import Any, Optional, Type
from pydantic import BaseModel, Field
import pandas as pd

from helpers.logger import logger
from services.vector_store import VectorStoreFactory


class WhatsAppChatMessagesRetrieverArgs(BaseModel):
    phone_number: str = Field(
        description="The phone number of the WhatsApp user")
    since: str = Field(
        description="The datetime from which to start retrieving. "
                    "Ex: 2024-10-05T00:00:00Z")
    until: Optional[str] = Field(
        description="The datetime until which to retrieve. "
                    "Ex: 2024-10-06T00:00:00Z")


class WhatsAppChatMessagesRetrieverTool(BaseTool):
    name: str = "Retrieve WhatsApp Chat Messages"
    description: str = """
      Retrieves WhatsApp chat messages from a specified phone number
      and returns a list containing the messages grouped by chat."""
    args_schema: Type[BaseModel] = WhatsAppChatMessagesRetrieverArgs
    vs: Optional[Any] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vs = VectorStoreFactory.get_vector_store(
            index_name="zapi-messages")

    def _run(self, phone_number: str, since: str, until: str = None) -> list:
        filter = {}

        begin = int(datetime.datetime.fromisoformat(since).timestamp() * 1000)
        filter["momment"] = {"$gte": begin}

        if until:
            end = int(
                datetime.datetime.fromisoformat(until).timestamp() * 1000)
            filter["momment"]["$lte"] = end

        logger.debug(f"Retrieving messages for {phone_number} "
                     f"using filter {filter}")

        results = self.vs.search(
            namespace=phone_number,
            filter=filter
        )
        logger.debug(f"\tNumber of messages retrieved: {len(results)}")

        return self._group_chat_messages(results)

    def _group_chat_messages(self, messages: list) -> list:
        df = pd.DataFrame([doc.dict() for doc in messages])

        # column metadata is a dictionary, expand it to columns
        df_metadata = pd.json_normalize(df['metadata'])

        # concat the metadata columns to the original dataframe
        # excluding the metadata column
        df = pd.concat([df, df_metadata], axis=1).drop(columns=['metadata'])

        # order by momment
        df = df.sort_values(by=['momment'])

        return df.groupby('chatName')['page_content'].apply(
            lambda x: "\n".join(x)).tolist()
