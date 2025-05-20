from typing import Optional

from pydantic import BaseModel


class Pet(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    type: str
    owner_id: Optional[int] = None
