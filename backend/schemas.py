from pydantic import BaseModel, UUID4
from typing import Optional


class TagBase(BaseModel):
    name: str
    value: str
    description: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None

class PromptBase(BaseModel):
    prompt: str
    