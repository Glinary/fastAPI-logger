import uvicorn

from fastapi import FastAPI

from app.routers.item import item_router

app = FastAPI()

# Include the item router
app.include_router(item_router, prefix="/items", tags=["items"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
