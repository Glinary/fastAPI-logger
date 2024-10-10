from pydantic import BaseModel
from typing import List

# TODO: Fill out the Pydantic Model with the fields: name (str) and description (str)
class Item(BaseModel):
    name: str
    description: str

from typing import List


# Request Models
class WebhookRequestData(BaseModel):
    object: str = ""
    entry: List = []
