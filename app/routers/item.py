from fastapi import APIRouter, Request
from ..service import create_item, read_item, update_item, delete_item, read_all_items
from ..model import Item

item_router = APIRouter()

# TODO: Create item POST "/"
@item_router.post("/")
async def create(item: Item):
    return create_item(item)

# TODO: Get all item GET "/"
@item_router.get("/")
async def get_all_items():
    return read_all_items()

# TODO: Get an item GET "/{item_id}"
@item_router.get("/{item_id}")
async def get_item(item_id: str):
    return read_item(item_id)

# TODO: Update an item PUT "/{item_id}"
@item_router.put("/{item_id}")
async def update(item_id: str, item: Item):
    return update_item(item_id, item)

# TODO: Delete an item DELETE "/{item_id}"
@item_router.delete("/{item_id}")
async def delete(item_id: str):
    return delete_item(item_id)