from pydantic import BaseModel
from typing import List

# Request Models
class WebhookRequestData(BaseModel):
    object: str = ""
    entry: List = []
