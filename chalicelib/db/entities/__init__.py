from pony.orm import Database, PrimaryKey, Required, Optional, Set
from uuid import UUID
from .histories import UserHistory, UserRoutineDayHistory, WorkoutHistory, ExerciseHistory, UserSchedulingHistory

muscle_core_db = Database()

class WeeklyDay: 
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class Visibility:
    PUBLIC = 0
    PRIVATE = 1
    FRIENDS = 2

class Difficulty:
    BEGINNER = 0
    INTERMEDIATE = 1
    ADVANCED = 2
    CBUM = 3


class User(muscle_core_db.Entity):
    _table_ = "user"
    user_id = PrimaryKey(UUID, column="user_id", nullable=False)
    email = Required(str, column="email", nullable=False)
    password = Required(str, column="password", nullable=False)
    created_at = Required(str, column="created_at", nullable=False)
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    role = Required(lambda: Role, column="role_id", nullable=False)

    user_workouts = Set(lambda: Workout)
    user_routines = Set(lambda: UserRoutineDay)
    user_weekly_routines = Set(lambda: UserWeeklyRoutine)
    user_schedulings = Set(lambda: UserScheduling)

    # histories
    user_histories = Set(lambda: UserHistory)
    user_exercise_histories = Set(lambda: ExerciseHistory)


class Role(muscle_core_db.Entity):
    _table_ = "role"
    role_id = PrimaryKey(UUID, column="role_id", nullable=False)
    name = Required(str, column="name", nullable=False)
    description = Optional(str, column="description", nullable=True)
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    users = Set(User)

class MuscularGroup(muscle_core_db.Entity):
    _table_ = "muscular_group"
    muscular_group_id = PrimaryKey(UUID, column="muscular_group_id", nullable=False)
    name = Required(str, column="name", nullable=False)
    description = Optional(str, column="description", nullable=True)
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    exercises = Set(lambda: Exercise)

class Exercise(muscle_core_db.Entity):
    _table_ = "exercise"
    exercise_id = PrimaryKey(UUID, column="exercise_id", nullable=False)
    name = Required(str, column="name", nullable=False)
    description = Optional(str, column="description", nullable=True)
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    muscular_group = Required(MuscularGroup, column="muscular_group_id")
    workouts = Set(lambda: Workout)

    guess_reps = Required(int, column="guess_reps", nullable=False)
    guess_sets = Required(int, column="guess_sets", nullable=False)
    guess_weight = Required(int, column="guess_weight", nullable=False)
    guess_rest_time = Required(int, column="guess_rest_time", nullable=False)
    guess_RM = Required(int, column="guess_RM", nullable=False)
    guess_RIR = Required(int, column="guess_RIR", nullable=False)

    difficulty = Required(int, column="difficulty", nullable=False, default=Difficulty.BEGINNER)

    history = Set(lambda: ExerciseHistory)

class Workout(muscle_core_db.Entity):
    _table_ = "workout"
    workout_id = PrimaryKey(UUID, column="workout_id", nullable=False)
    users = Set(User, column="user_id")
    name = Required(str, column="name", nullable=False)
    description = Optional(str, column="description", nullable=True)
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    exercises = Set(lambda: Exercise)
    user_routines = Set(lambda: UserRoutineDay)
    visibility = Required(int, column="visibility", nullable=False, default=Visibility.PRIVATE)
    difficulty = Required(int, column="difficulty", nullable=False, default=Difficulty.BEGINNER)

    history = Set(lambda: WorkoutHistory)

class UserRoutineDay(muscle_core_db.Entity):
    _table_ = "user_routine"
    user_routine_id = PrimaryKey(UUID, column="user_routine_id", nullable=False)
    user = Required(User, column="user_id")
    workouts = Set(Workout, column="workout_id")
    week_day = Required(int, column="week_day", nullable=False, default=WeeklyDay.MONDAY)
    name = Required(str, column="name", nullable=False)
    description = Optional(str, column="description", nullable=True)
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    created_at = Required(str, column="created_at", nullable=False)
    updated_at = Optional(str, column="updated_at", nullable=True)
    user_weekly_routines = Set(lambda: UserWeeklyRoutine)

    history = Set(lambda: UserRoutineDayHistory)

class UserWeeklyRoutine(muscle_core_db.Entity):
    _table_ = "user_weekly_routine"
    user_weekly_routine_id = PrimaryKey(UUID, column="user_weekly_routine_id", nullable=False)
    user = Required(User, column="user_id")
    user_routine_days = Set(UserRoutineDay, column="user_routines_id")
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    created_at = Required(str, column="created_at", nullable=False)
    updated_at = Optional(str, column="updated_at", nullable=True)
    sort_order = Required(int, column="sort_order", nullable=False)
    user_scheduling = Required(lambda: UserScheduling, column="user_scheduling_id")

    history_scheduling = Set(lambda: UserSchedulingHistory)

class UserScheduling(muscle_core_db.Entity):
    _table_ = "user_scheduling"
    user_scheduling_id = PrimaryKey(UUID, column="user_scheduling_id", nullable=False)
    user = Required(User, column="user_id")
    user_weekly_routines = Set(UserWeeklyRoutine, column="user_weekly_routine_id")
    is_active = Required(bool, column="is_active", nullable=False, default=True)
    created_at = Required(str, column="created_at", nullable=False)
    updated_at = Optional(str, column="updated_at", nullable=True)

    history = Set(lambda: UserSchedulingHistory)
    