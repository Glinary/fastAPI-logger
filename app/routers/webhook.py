from fastapi import APIRouter, Request
from ..service import verify_webhook, webhook
from ..model import WebhookRequestData

webhook_router = APIRouter()

@webhook_router.get("/webhook")
async def verify(request: Request):
    return verify_webhook(request)

@webhook_router.post("/webhook")
async def webhook(data: WebhookRequestData):
    return webhook(data)