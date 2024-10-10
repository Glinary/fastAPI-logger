import uvicorn
from fastapi import FastAPI
from app.routers.item import item_router
from app.routers.webhook import webhook_router

app = FastAPI()

# Include the item router
app.include_router(item_router, prefix="/items", tags=["items"])
app.include_router(webhook_router, prefix="/api", tags=["webhook"])

if __name__ == "__main__":
    # Start the Uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8000)
