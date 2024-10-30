from fastapi import APIRouter, Request
from ..services.service import verify_webhook, handle_webhook
from ..models.model import WebhookRequestData

webhook_router = APIRouter()

@webhook_router.get("/webhook")
async def verify(request: Request):
    return verify_webhook(request)

@webhook_router.post("/webhook")
async def webhook(data: WebhookRequestData):
    return await handle_webhook(data)