import logging
from fastapi import FastAPI
import uvicorn

from services.vector_store import VectorStoreFactory

from .models import WhatsAppMessage


app = FastAPI()

# FIXME
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.post("/receive")
async def receive_whatsapp_message(message: WhatsAppMessage):
    try:
        logger.debug(f"Received message from {message.senderName}: "
                     f"{message}")

        vs = VectorStoreFactory.get_vector_store(index_name="zapi-messages")

        vs.add_message(message)

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing the message: {e}")
        return {"status": "error", "message": str(e)}


@app.get("/")
async def root():
    return {"message": "WhatsApp Webhook is running"}


def run():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")


if __name__ == "__main__":
    run()
