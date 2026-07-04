"""Pydantic schema for teleop-period scouting entries (2025 Reefscape)."""

from pydantic import BaseModel, ConfigDict
from typing import Optional

class TeleopScout(BaseModel):
    """Request body for ``POST /scout/add/teleop/2025``.

    Represents a single scout's observations of one team's teleop period
    (plus endgame climb) during one match, mapping directly onto the
    ``teleop_scout_reefscape`` table (see ``sql/database-schema.sql``).

    :ivar event_key: TBA event key, e.g. ``"2025sao"``.
    :ivar match_key: TBA match key, e.g. ``"2025sao_qm12"``.
    :ivar team_key: TBA team key, e.g. ``"frc7563"``.
    :ivar year: Competition season year.
    :ivar l1: Coral scored on reef level 1 during teleop.
    :ivar l2: Coral scored on reef level 2 during teleop.
    :ivar l3: Coral scored on reef level 3 during teleop.
    :ivar l4: Coral scored on reef level 4 during teleop.
    :ivar coral_misseds: Number of missed coral scoring attempts.
    :ivar coral_precision: Coral scoring accuracy, expressed as a
        percentage (0-100).
    :ivar algae_removed: Algae removed from the reef during teleop.
    :ivar algae_net: Algae scored in the net during teleop.
    :ivar algae_processor: Algae scored in the processor during teleop.
    :ivar climb: Endgame climb result (e.g. ``"deep"``, ``"shallow"``,
        ``"park"``, ``"none"`` — free-text, not constrained by an enum).
    :ivar collected_coral_floor: Whether the robot picked up coral from
        the floor.
    :ivar collected_coral_station: Whether the robot picked up coral from
        the human player station.
    :ivar collected_algae_reef: Whether the robot picked algae off the
        reef.
    :ivar issues: Whether the robot experienced any issues/malfunctions.
    :ivar issues_notes: Free-text description of the issue(s), if any.
    :ivar defended: Whether the robot played defense during the match.
    :ivar driver_rating: Subjective 1-N rating of driver skill (no
        hard-coded bounds are enforced at the schema level).
    :ivar score: Computed/estimated teleop score contribution for this
        team.
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