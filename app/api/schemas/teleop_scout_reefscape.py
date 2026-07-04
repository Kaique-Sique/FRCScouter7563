from pydantic import BaseModel, ConfigDict
from typing import Optional

class TeleopScout(BaseModel):
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

    climb: str | None = None

    collected_coral_floor: bool = False
    collected_coral_station: bool = False
    collected_algae_reef: bool = False

    issues: bool = False
    issues_notes: str | None = None

    defended: bool = False

    driver_rating: int | None = None

    score: int = 0

    notes: str | None = None