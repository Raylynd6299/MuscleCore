from datetime import datetime
from pony.orm import  PrimaryKey, Required, Optional, Set
from uuid import UUID
from chalicelib.db.entities import muscle_core_db, User, UserRoutineDay, UserScheduling, UserWeeklyRoutine, Workout, Exercise

class UserSchedulingHistory(muscle_core_db.Entity):
    _table_ = "user_scheduling_history"
    user_scheduling_history_id = PrimaryKey(UUID, column="user_scheduling_history_id", nullable=False)
    user_scheduling = Required(UserScheduling, column="user_scheduling_id")
    user_weekly_routine = Required(UserWeeklyRoutine, column="user_weekly_routine_id")
    sort_order = Required(int, column="sort_order", nullable=False)
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    created_at = Required(str, column="created_at", nullable=False)
    updated_at = Optional(str, column="updated_at", nullable=True)  

class UserRoutineDayHistory(muscle_core_db.Entity):
    _table_ = "user_routine_history"
    user_routine_history_id = PrimaryKey(UUID, column="user_routine_history_id", nullable=False)
    user_routine = Required(UserRoutineDay, column="user_routine_id")
    created_at = Required(datetime, column="created_at", nullable=False)
    updated_at = Optional(datetime, column="updated_at", nullable=True)
    workout_time = Required(int, column="workout_time", nullable=False)
    workout_history = Set(lambda: WorkoutHistory)

class WorkoutHistory(muscle_core_db.Entity):
    _table_ = "workout_history"
    workout_history_id = PrimaryKey(UUID, column="workout_history_id", nullable=False)
    user_routine_day_history = Required(UserRoutineDayHistory, column="user_routine_day_history_id")
    workout = Required(Workout, column="workout_id")
    created_at = Required(datetime, column="created_at", nullable=False)
    updated_at = Optional(datetime, column="updated_at", nullable=True)
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    description = Optional(str, column="description", nullable=True)
    exercises = Set(lambda: ExerciseHistory)

class ExerciseHistory(muscle_core_db.Entity):
    _table_ = "exercise_history"
    exercise_history_id = PrimaryKey(UUID, column="exercise_history_id", nullable=False)
    use = Required(User, column="user_id")
    workout_history = Required(WorkoutHistory, column="workout_history_id")
    exercise = Required(Exercise, column="exercise_id")
    created_at = Required(datetime, column="created_at", nullable=False)
    updated_at = Optional(datetime, column="updated_at", nullable=True)
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    description = Optional(str, column="description", nullable=True)
    reps = Required(int, column="reps", nullable=False)
    sets = Required(int, column="sets", nullable=False)
    weight = Required(int, column="weight", nullable=False)
    rest_time = Required(int, column="rest_time", nullable=False)
    RM = Required(int, column="RM", nullable=False)
    RIR = Required(int, column="RIR", nullable=False)

class UserHistory(muscle_core_db.Entity):
    _table_ = "user_history"
    user_history_id = PrimaryKey(UUID, column="user_history_id", nullable=False)
    user = Required(User, column="user_id")
    created_at = Required(datetime, column="created_at", nullable=False)