from pydantic import BaseModel, ConfigDict
from typing import Optional

class PitScout(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_key: str
    team_key: str
    description: str | None = None
    img_url: str | None = None