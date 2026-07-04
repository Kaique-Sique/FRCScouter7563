from pydantic import BaseModel, ConfigDict
from typing import Optional

class AutoScout(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_key: str
    match_key: str
    team_key: str
    year: int

    l1: int = 0
    l2: int = 0
    l3: int = 0
    l4: int = 0

    coral_misseds: int = 0
    coral_precision: float = 0

    algae_removed: int = 0
    algae_net: int = 0
    algae_processor: int = 0

    region_scored: dict | None = None

    score: int = 0

    startline: bool = False

    notes: str | None = None