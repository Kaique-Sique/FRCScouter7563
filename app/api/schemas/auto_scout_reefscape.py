"""Pydantic schema for autonomous-period scouting entries (2025 Reefscape)."""

from pydantic import BaseModel, ConfigDict
from typing import Optional

class AutoScout(BaseModel):
    """Request body for ``POST /scout/add/auto/2025``.

    Represents a single scout's observations of one team's autonomous
    period during one match, mapping directly onto the
    ``auto_scout_reefscape`` table (see ``sql/database-schema.sql``).

    :ivar event_key: TBA event key, e.g. ``"2025sao"``.
    :ivar match_key: TBA match key, e.g. ``"2025sao_qm12"``.
    :ivar team_key: TBA team key, e.g. ``"frc7563"``.
    :ivar year: Competition season year.
    :ivar l1: Coral scored on reef level 1 during auto.
    :ivar l2: Coral scored on reef level 2 during auto.
    :ivar l3: Coral scored on reef level 3 during auto.
    :ivar l4: Coral scored on reef level 4 during auto.
    :ivar coral_misseds: Number of missed coral scoring attempts.
    :ivar coral_precision: Coral scoring accuracy, expressed as a
        percentage (0-100).
    :ivar algae_removed: Algae removed from the reef during auto.
    :ivar algae_net: Algae scored in the net during auto.
    :ivar algae_processor: Algae scored in the processor during auto.
    :ivar region_scored: Free-form JSON payload describing *where* on the
        field scoring occurred (e.g. per-branch/region breakdown),
        stored as ``JSONB`` in Postgres.
    :ivar score: Computed/estimated auto score contribution for this team.
    :ivar startline: Whether the robot left the starting line (mobility).
    :ivar notes: Free-text scouting notes.
    """

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