from bson import ObjectId
from fastapi import HTTPException
from .mongodb import collection
from .model import Item


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
