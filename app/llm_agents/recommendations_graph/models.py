from typing import Annotated, Any

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class State(BaseModel):
    messages: Annotated[list[Any], add_messages] = Field(default=[])
    location: str
    traveller_profile: str
