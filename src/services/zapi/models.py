from pydantic import BaseModel
from typing import Optional


class TextMessage(BaseModel):
    message: str
    description: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    thumbnailUrl: Optional[str] = None

    class Config:
        extra = 'allow'


class ReferenceMessage(BaseModel):
    messageId: str
    fromMe: bool
    phone: str
    participant: Optional[str] = None


class Reaction(BaseModel):
    value: str
    time: int
    reactionBy: str
    referencedMessage: ReferenceMessage


class WhatsAppMessage(BaseModel):
    messageId: str
    fromMe: bool
    phone: str
    connectedPhone: str
    waitingMessage: bool
    isGroup: bool
    isNewsletter: bool
    instanceId: str
    momment: int
    status: str
    chatName: str
    senderName: str
    broadcast: bool
    forwarded: bool
    type: str
    fromApi: bool
    isStatusReply: Optional[bool] = None
    chatLid: Optional[str] = None
    isEdit: Optional[bool] = None
    senderPhoto: Optional[str] = None
    photo: Optional[str]
    participantLid: Optional[str] = None
    referenceMessageId: Optional[str] = None
    text: Optional[TextMessage] = None
    reaction: Optional[Reaction] = None
