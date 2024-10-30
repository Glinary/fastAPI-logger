import logging

from bson import ObjectId
from fastapi import HTTPException, Request, Response
from ..models.model import WebhookRequestData
import os
import httpx
from dotenv import load_dotenv
from ..utils.llama_webhook import OpenWebUIClient
from ..utils.dynamodb import DynamoDBLogger

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the environment variables
load_dotenv()
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
OPENWEBUI_API = os.getenv('OPENWEBUI_API')

"""
    Verifies the webhook using a valid verification token. Also checks the
    validity of the webhook given Facebook's template for chatbots.

    Arguments:
        request: (Request) contains the request class to be verified by the webhook

"""
async def verify_webhook(request: Request):
    logger.info("Verifying webhook request...")
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get("hub.challenge"):
        if (not request.query_params.get("hub.verify_token") == VERIFICATION_TOKEN):
            logger.warning("Verification token mismatch.")
            return Response(content="Verification token mismatch", status_code=403)
        logger.info("Webhook verified successfully.")
        return Response(content=request.query_params["hub.challenge"])
        
    logger.error("Webhook verification failed. Required arguments are missing.")
    return Response(content="Required arguments haven't passed.", status_code=400)

"""
    Send message to specific user(By recipient ID) from specific page(By
    access token).

    Arguments:
        page_access_token: (string) Target page access token.
        recipient_id: (string) The ID of the user that the message is
         addressed to.
        message_text: (string) The content of the message.
        message_type: (string) The type of the target message.
         RESPONSE, UPDATE or MESSAGE_TAG - the accurate description -
         https://developers.facebook.com/docs/messenger-platform/send-messages/#messaging_types
"""
async def send_message(
    page_access_token: str,
    recipient_id: str,
    message_text: str,
    message_type: str = "UPDATE",
):
    try:
        logger.info(f"Sending message to recipient_id: {recipient_id}")
        r = httpx.post(
            "https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": page_access_token},
            headers={"Content-Type": "application/json"},
            json={
                "recipient": {"id": recipient_id},
                "message": {"text": message_text},
                "messaging_type": message_type,
            },
        )
        r.raise_for_status()
        logger.info(f"Message sent to recipient_id: {recipient_id}")
    except httpx.HTTPStatusError as exc:
        logger.error(f"HTTP error occurred while sending message: {exc}")
    except Exception as exc:
        logger.error(f"An unexpected error occurred while sending message: {exc}")

"""
    Saves the logs of the user in a dynamoDB schema.

    Arguments:
        sender_id: (string) the ID of the sender
        text: (string) the content of the message
        timestamp: (string) the message's timestamp
        event_type: (string) event type to identify whether it is a user or a bot
"""
def save_logs(sender_id: str, text: str, timestamp: str, event_type: str):
    logger.info(f"Saving user logs for sender_id: {sender_id}")
    try:
        dynamoDB = DynamoDBLogger()
        dynamoDB.log_item(sender_id=sender_id, timestamp=str(timestamp), text=text, event_type=event_type)
        logger.info(f"User logs saved for sender_id: {sender_id}")
    except Exception as exc:
        logger.error(f"Error saving user logs for sender_id: {sender_id} - {exc}")

"""
    Handles webhook data and sends responses using the OpenWebUI client.

    Arguments:
        data: (WebHookRequestData) contains the WebhookRequestData class to be handled by the webhook
"""
async def handle_webhook(data: WebhookRequestData):
    api_url = "http://localhost:3000/api/chat/completions"
    client = OpenWebUIClient(api_url=api_url, api_key=OPENWEBUI_API)
    
    logger.info("Handling webhook data...")
    if data.object == "page":
        for entry in data.entry:
            messaging_events = [
                event for event in entry.get("messaging", []) if event.get("message")
            ]
            for event in messaging_events:
                message = event.get("message")
                timestamp = event.get("timestamp")
                user_id = event["sender"]["id"]
                recipient_id = event["recipient"]["id"]

                logger.info(f"Processing message from user_id: {user_id}")
                client.set_user_message(message['text'])

                try:
                    response = client.send_request()
                    logger.info(f"Received response from OpenWebUI for user_id: {user_id}")
                except Exception as exc:
                    logger.error(f"Error sending request to OpenWebUI: {exc}")
                    continue

                bot_message = response["choices"][0]["message"]["content"]

                await send_message(page_access_token=PAGE_ACCESS_TOKEN,
                                   recipient_id=user_id,
                                   message_text=f"{bot_message}")
                
                save_logs(user_id, message['text'], timestamp, "user")
                save_logs(recipient_id, bot_message, timestamp, "bot")
                
            
    return Response(content="ok")