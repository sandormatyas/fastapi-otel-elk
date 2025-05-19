from pydantic import BaseModel
from typing import Optional


class Pet(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    type: str
    owner_id: Optional[int] = None
