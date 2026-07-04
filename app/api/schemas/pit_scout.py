"""Pydantic schema for pit scouting entries."""

from pydantic import BaseModel, ConfigDict
from typing import Optional

class PitScout(BaseModel):
    """Request body for ``POST /scout/add/pit/``.

    Represents pre-match "pit scouting" data collected once per team per
    event (robot description, photo, etc), mapping onto the ``pit_scout``
    table (see ``sql/database-schema.sql``).

    :ivar event_key: TBA event key, e.g. ``"2025sao"``.
    :ivar team_key: TBA team key, e.g. ``"frc7563"``.
    :ivar description: Free-text description of the robot/team
        (drivetrain, mechanisms, strategy, etc).
    :ivar img_url: URL to a photo of the robot.
    """

    model_config = ConfigDict(from_attributes=True)

    event_key: str
    team_key: str
    description: str | None = None
    img_url: str | None = None