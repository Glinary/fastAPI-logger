from pydantic import BaseModel


# TODO: Fill out the Pydantic Model with the fields: name (str) and description (str)
class Item(BaseModel):
    name: str
    description: str
