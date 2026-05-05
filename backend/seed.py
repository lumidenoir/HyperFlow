#!/usr/bin/env python3
"""
Seed script to populate the database with sample exercises and a test workout.
Useful for testing the API without manual data entry.
"""

from datetime import datetime, timedelta
from sqlmodel import Session, create_engine

from models import Exercise, MuscleState, WorkoutSession, SetLog

# Use same database path
sqlite_url = "sqlite:///./data/gym.db"
engine = create_engine(sqlite_url, echo=True)


def seed_exercises():
    """Create sample exercises."""
    with Session(engine) as session:
        exercises = [
            # Chest
            Exercise(
                name="Dumbbell Bench Press",
                primary_muscle="Chest",
                secondary_muscle="Triceps",
                fatigue_rating=1.8,
                notes="Primary chest builder - from yaml",
            ),
            Exercise(
                name="Dumbbell Flyovers",
                primary_muscle="Chest",
                secondary_muscle="Shoulders",
                fatigue_rating=1.4,
                notes="Isolation and stretch - from yaml",
            ),
            Exercise(
                name="Push-ups",
                primary_muscle="Chest",
                secondary_muscle="Triceps",
                fatigue_rating=1.2,
                notes="Classic bodyweight push",
            ),
            # Back
            Exercise(
                name="Dumbbell Row",
                primary_muscle="Back",
                secondary_muscle="Biceps",
                fatigue_rating=1.6,
                notes="Unilateral back strength - from yaml",
            ),
            Exercise(
                name="Pendlay Rows (DB)",
                primary_muscle="Back",
                secondary_muscle="Biceps",
                fatigue_rating=1.8,
                notes="Explosive pull from floor - from yaml",
            ),
            Exercise(
                name="Dumbbell Pullovers",
                primary_muscle="Back",
                secondary_muscle="Chest",
                fatigue_rating=1.5,
                notes="Lat stretch focus - from yaml",
            ),
            Exercise(
                name="Pull-ups",
                primary_muscle="Back",
                secondary_muscle="Biceps",
                fatigue_rating=2.0,
                notes="Bodyweight vertical pull",
            ),
            # Legs
            Exercise(
                name="Bulgarian Split Squats",
                primary_muscle="Legs",
                secondary_muscle="Glutes",
                fatigue_rating=2.5,
                notes="Brutal unilateral leg builder - from yaml",
            ),
            Exercise(
                name="Dumbbell Lunges",
                primary_muscle="Legs",
                secondary_muscle="Glutes",
                fatigue_rating=2.0,
                notes="Walking or static - from yaml",
            ),
            Exercise(
                name="Cossack Squats",
                primary_muscle="Legs",
                fatigue_rating=1.6,
                notes="Mobility and quad strength - from yaml",
            ),
            Exercise(
                name="RDL (Dumbbell)",
                primary_muscle="Legs",
                secondary_muscle="Back",
                fatigue_rating=2.0,
                notes="Hamstring/Glute hinge - from yaml",
            ),
            Exercise(
                name="Calf Raises",
                primary_muscle="Legs",
                fatigue_rating=1.0,
                notes="Standing or seated - from yaml",
            ),
            # Shoulders
            Exercise(
                name="Dumbbell Overhead Press",
                primary_muscle="Shoulders",
                secondary_muscle="Triceps",
                fatigue_rating=1.8,
                notes="Vertical push",
            ),
            Exercise(
                name="Dumbbell Lateral Raises",
                primary_muscle="Shoulders",
                fatigue_rating=1.2,
                notes="Side delt isolation",
            ),
            # Biceps
            Exercise(
                name="Zottman Curls",
                primary_muscle="Biceps",
                secondary_muscle="Forearms",
                fatigue_rating=1.4,
                notes="Bicep and brachialis - from yaml",
            ),
            Exercise(
                name="Dumbbell Curls",
                primary_muscle="Biceps",
                fatigue_rating=1.2,
                notes="Standard arm builder",
            ),
            # Triceps
            Exercise(
                name="Bench Dips",
                primary_muscle="Triceps",
                secondary_muscle="Chest",
                fatigue_rating=1.3,
                notes="Bodyweight tricep focus - from yaml",
            ),
            Exercise(
                name="Dumbbell Kickbacks",
                primary_muscle="Triceps",
                fatigue_rating=1.0,
                notes="Tricep isolation - from yaml",
            ),
            # Core
            Exercise(
                name="Bicycle Crunches",
                primary_muscle="Core",
                fatigue_rating=1.0,
                notes="Oblique focus - from yaml",
            ),
            Exercise(
                name="Reverse Crunches",
                primary_muscle="Core",
                fatigue_rating=1.0,
                notes="Lower ab focus - from yaml",
            ),
            Exercise(
                name="Weighted Situps",
                primary_muscle="Core",
                fatigue_rating=1.2,
                notes="Upper ab loaded - from yaml",
            ),
        ]

        for ex in exercises:
            session.add(ex)
        session.commit()
        print(f"✓ Created {len(exercises)} bodyweight and dumbbell exercises")


def seed_test_workout():
    """Create a sample DB/Bodyweight workout from yesterday."""
    with Session(engine) as session:
        # Create a session from yesterday
        yesterday = datetime.now() - timedelta(days=1)
        workout = WorkoutSession(
            date=yesterday,
            status="completed",
            notes="YAML Routine Day 1",
            duration_minutes=55,
        )
        session.add(workout)
        session.flush()  # Get the ID

        # Get the new exercises
        db_press = (
            session.query(Exercise).filter_by(name="Dumbbell Bench Press").first()
        )
        db_flyovers = (
            session.query(Exercise).filter_by(name="Dumbbell Flyovers").first()
        )
        bench_dips = session.query(Exercise).filter_by(name="Bench Dips").first()
        zottman = session.query(Exercise).filter_by(name="Zottman Curls").first()
        db_row = session.query(Exercise).filter_by(name="Dumbbell Row").first()

        # Create set logs with DB weights instead of barbell weights
        sets = [
            SetLog(
                session_id=workout.id,
                exercise_id=db_press.id,
                reps=10,
                weight=50,
                rpe=8,
            ),
            SetLog(
                session_id=workout.id,
                exercise_id=db_press.id,
                reps=10,
                weight=50,
                rpe=8,
            ),
            SetLog(
                session_id=workout.id, exercise_id=db_press.id, reps=8, weight=50, rpe=9
            ),
            SetLog(
                session_id=workout.id,
                exercise_id=db_flyovers.id,
                reps=10,
                weight=25,
                rpe=7,
            ),
            SetLog(
                session_id=workout.id,
                exercise_id=db_flyovers.id,
                reps=10,
                weight=25,
                rpe=8,
            ),
            SetLog(
                session_id=workout.id, exercise_id=db_row.id, reps=10, weight=45, rpe=7
            ),
            SetLog(
                session_id=workout.id, exercise_id=db_row.id, reps=10, weight=45, rpe=8
            ),
            SetLog(
                session_id=workout.id, exercise_id=db_row.id, reps=10, weight=45, rpe=8
            ),
            SetLog(
                session_id=workout.id, exercise_id=zottman.id, reps=12, weight=20, rpe=7
            ),
            SetLog(
                session_id=workout.id, exercise_id=zottman.id, reps=10, weight=20, rpe=8
            ),
            SetLog(
                session_id=workout.id,
                exercise_id=bench_dips.id,
                reps=15,
                weight=0,
                rpe=7,
            ),
            SetLog(
                session_id=workout.id,
                exercise_id=bench_dips.id,
                reps=12,
                weight=0,
                rpe=8,
            ),
        ]

        for s in sets:
            session.add(s)

        session.commit()
        print(f"✓ Created test workout with {len(sets)} sets")


def clear_database():
    """WARNING: Clears all data. Use with caution."""
    from models import SQLModel
    from sqlmodel import text

    with Session(engine) as session:
        # Drop all tables
        SQLModel.metadata.drop_all(engine)
        print("✓ Database cleared")


if __name__ == "__main__":
    import sys

    # Initialize tables
    from models import SQLModel

    SQLModel.metadata.create_all(engine)
    print("✓ Tables created")

    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_database()
        # Re-create tables after clearing
        SQLModel.metadata.create_all(engine)

    seed_exercises()
    seed_test_workout()
    print("\n✓ Database seeded successfully!")
