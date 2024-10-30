import logging

import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenWebUIClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.payload = {
            "model": "llama3.1:latest",
            "messages": []
        }
        logger.info(f"OpenWebUIClient initialized with API URL: {self.api_url}")

    def set_user_message(self, message):
        """Set or update the user's message in the prompt."""
        self.payload['messages'] = [
            {
                "role": "user",
                "content": message
            }
        ]
        logger.info(f"User message set: {message}")

    def send_request(self):
        """Send the request to the API and return the response."""
        try:
            logger.info("Sending request to OpenWebUI API...")
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(self.payload))

            if response.status_code == 200:
                logger.info("Request successful.")
                return response.json()
            else:
                logger.error(f"API call failed. Status code: {response.status_code}, Response: {response.text}")
                return f"Failed to call API. Status code: {response.status_code}, Response: {response.text}"
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while sending the request: {e}")
            return f"An error occurred: {e}"
