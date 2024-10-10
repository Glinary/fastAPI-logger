from bson import ObjectId
from fastapi import HTTPException, Request, Response
from .mongodb import collection
from .model import Item, WebhookRequestData
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')

def item_helper(item) -> dict:
    if isinstance(item, list):
        return [item_helper(i) for i in item]
    else:
        return {
            "id": str(item["_id"]),
            "name": item["name"],
            "description": item["description"],
        }

# TODO: Insert an item and return the created item
def create_item(item: Item):
    item_dict = item.dict()
    result = collection.insert_one(item_dict)
    created_item = collection.find_one({"_id": result.inserted_id})
    return item_helper(created_item)


# TODO: Find an item using the item id
def read_item(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_helper(item)


# TODO: Find all item and make it a list for item_helper. Hint: check the return type.
def read_all_items():
    items = collection.find()
    if items is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_helper(list(items))


# TODO: Update an item using item id and item payload
def update_item(item_id: str, item: Item):

    updated_item = collection.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict()},
        return_document=True
    )
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_helper(updated_item)


# TODO: delete an item using item id
def delete_item(item_id: str):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}

def verify_webhook(request: Request):
    print(f'verificationtoken: {VERIFICATION_TOKEN}')
    print(f'hubmode: {request.query_params.get("hub.mode")}')
    print(f'hubchallenge: {request.query_params.get("hub_challenge")}')
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get("hub.challenge"):
        if (not request.query_params.get("hub.verify_token") == VERIFICATION_TOKEN):
            return Response(content="Verification token mismatch", status_code=403)
        return Response(content=request.query_params["hub.challenge"])
        
    return Response(content="Required arguments haven't passed.", status_code=400)

# Helpers.
async def send_message(
    page_access_token: str,
    recipient_id: str,
    message_text: str,
    message_type: str = "UPDATE",
):
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
    
async def webhook(data: WebhookRequestData):
    """
    Messages handler.
    """
    if data.object == "page":
        for entry in data.entry:
            messaging_events = [
                event for event in entry.get("messaging", []) if event.get("message")
            ]
            for event in messaging_events:
                message = event.get("message")
                sender_id = event["sender"]["id"]

                await send_message(page_access_token=os.environ["PAGE_ACCESS_TOKEN"],
                                   recipient_id=sender_id,
                                   message_text=f"echo: {message['text']}")

    return Response(content="ok")