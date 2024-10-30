import logging
import uvicorn
from fastapi import FastAPI
from app.routers.webhook import webhook_router

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Include the webhook router
app.include_router(webhook_router, prefix="/api", tags=["webhook"])
logger.info("Webhook router included with prefix '/api'")

if __name__ == "__main__":
    # Start the Uvicorn server
    logger.info("Starting Uvicorn server at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
