from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

# --- Constants ---
FATIGUE_LIMIT = 10.0  # Max fatigue before a muscle is "red-zoned"
DECAY_K = 0.5  # Recovery rate (higher = faster recovery)


class Exercise(SQLModel, table=True):
    """Represents a single exercise with muscle targets and fatigue rating."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=100)
    primary_muscle: str = Field(min_length=1, max_length=50)
    secondary_muscle: Optional[str] = Field(default=None, max_length=50)
    fatigue_rating: float = Field(default=1.0, ge=0.1, le=10.0)  # Base fatigue per set
    notes: Optional[str] = Field(default=None, max_length=500)


class MuscleState(SQLModel, table=True):
    """Tracks current fatigue and recovery state per muscle group."""

    muscle_group: str = Field(primary_key=True, min_length=1, max_length=50)
    current_fatigue: float = Field(default=0.0, ge=0.0)
    last_updated: datetime = Field(default_factory=datetime.now)


class WorkoutSession(SQLModel, table=True):
    """Represents a complete workout session."""

    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.now, index=True)
    status: str = Field(default="draft")  # Default is now 'draft' instead of 'active'
    notes: Optional[str] = Field(default=None, max_length=500)
    duration_minutes: Optional[int] = Field(default=None, ge=0)
    planned_template: str = Field(default="[]")


class SetLog(SQLModel, table=True):
    """Individual set within a workout session."""

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="workoutsession.id", index=True)
    exercise_id: int = Field(foreign_key="exercise.id")
    reps: int = Field(ge=1, le=100)
    weight: float = Field(ge=0.0, le=10000.0)
    rpe: Optional[int] = Field(
        default=None, ge=1, le=10
    )  # Rate of Perceived Exertion (1-10)
    notes: Optional[str] = Field(default=None, max_length=200)
    logged_at: datetime = Field(default_factory=datetime.now)


class WorkoutSummary(SQLModel):
    """DTO for returning workout summary data (no table)."""

    id: int
    date: datetime
    duration_minutes: Optional[int]
    total_sets: int
    total_volume: float
    exercises_count: int
    notes: Optional[str]
