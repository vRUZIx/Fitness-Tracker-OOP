"""
Validation script for Sprint 2 implementation.
Verifies all components are working correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.user import User
from models.workout import Workout
from models.factory import ObjectFactory
from services.user_service import UserService
from services.workout_service import WorkoutService
from services.scheduler import Scheduler
from strategies.calorie_strategy import SimpleCalorieStrategy, ConstantBurnStrategy
from strategies.intensity_strategy import AgeBasedIntensityStrategy, DurationBasedIntensityStrategy
from repository.repository import Repository
import tempfile


def test_crud_operations():
    """Test complete CRUD operations."""
    print("Testing CRUD operations...")
    
    # Create temp repository
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    repo = Repository(filename=path)
    
    user_service = UserService(repo=repo)
    workout_service = WorkoutService(repo=repo)
    
    # CREATE
    user_id = user_service.create_user("Test User", 30, height=175.0, weight=70.0)
    workout_id = workout_service.create_workout("Test Workout", 45)
    print(f"✓ Created user: {user_id}")
    print(f"✓ Created workout: {workout_id}")
    
    # READ
    user_record = user_service.read_record(user_id)
    workout_record = workout_service.read_record(workout_id)
    assert user_record is not None
    assert workout_record is not None
    print("✓ Read operations successful")
    
    # UPDATE
    user_service.update_user(user_id, age=31, weight=68.0)
    workout_service.update_workout(workout_id, duration=50)
    updated_user = user_service.read_record(user_id)
    updated_workout = workout_service.read_record(workout_id)
    assert updated_user["data"]["age"] == 31
    assert updated_workout["data"]["duration"] == 50
    print("✓ Update operations successful")
    
    # DELETE
    user_service.delete_user(user_id)
    workout_service.delete_workout(workout_id)
    assert user_service.read_record(user_id) is None
    assert workout_service.read_record(workout_id) is None
    print("✓ Delete operations successful")
    
    # Cleanup
    os.unlink(path)
    print("✓ CRUD operations: PASSED\n")


def test_strategies():
    """Test strategy patterns."""
    print("Testing strategy patterns...")
    
    user = User("Alice", 30, height=170.0, weight=65.0)
    workout = Workout("Cardio", 45)
    
    # Calorie strategies
    simple_strategy = SimpleCalorieStrategy(met=6.0)
    calories_simple = simple_strategy.calculate(user, workout)
    print(f"✓ Simple strategy: {calories_simple:.1f} kcal")
    
    constant_strategy = ConstantBurnStrategy(rate_per_min=5.0)
    calories_constant = constant_strategy.calculate(user, workout)
    print(f"✓ Constant strategy: {calories_constant:.1f} kcal")
    
    # Intensity strategies
    age_strategy = AgeBasedIntensityStrategy()
    intensity_age = age_strategy.calculate_intensity(user, workout)
    print(f"✓ Age-based intensity: {intensity_age}")
    
    duration_strategy = DurationBasedIntensityStrategy()
    intensity_duration = duration_strategy.calculate_intensity(user, workout)
    print(f"✓ Duration-based intensity: {intensity_duration}")
    
    print("✓ Strategy patterns: PASSED\n")


def test_factory_pattern():
    """Test factory pattern."""
    print("Testing factory pattern...")
    
    user = ObjectFactory.create_object("user", "Bob", 25)
    workout = ObjectFactory.create_object("workout", "Running", 30)
    
    assert user.username == "Bob"
    assert workout.name == "Running"
    print("✓ Factory object creation successful")
    
    user_record = {"type": "user", "data": {"username": "Charlie", "age": 35}}
    workout_record = {"type": "workout", "data": {"name": "Swimming", "duration": 40}}
    
    user_obj = ObjectFactory.create_from_record(user_record)
    workout_obj = ObjectFactory.create_from_record(workout_record)
    
    assert user_obj.username == "Charlie"
    assert workout_obj.name == "Swimming"
    print("✓ Factory from record successful")
    print("✓ Factory pattern: PASSED\n")


def test_scheduler():
    """Test scheduler with strategies."""
    print("Testing scheduler...")
    
    scheduler = Scheduler()
    user = User("Dave", 40, height=180.0, weight=80.0)
    workout = Workout("Weights", 60)
    
    # No strategy
    result = scheduler.schedule_workout(user, workout)
    assert "scheduled" in result.lower()
    print("✓ Scheduling without strategy successful")
    
    # With simple strategy
    result = scheduler.schedule_workout(user, workout, strategy="simple", met=5.0)
    assert "calories" in result.lower()
    print("✓ Scheduling with simple strategy successful")
    
    # With constant strategy
    result = scheduler.schedule_workout(user, workout, strategy="constant", rate_per_min=4.0)
    assert "calories" in result.lower()
    print("✓ Scheduling with constant strategy successful")
    
    print("✓ Scheduler: PASSED\n")


def test_validation():
    """Test input validation."""
    print("Testing input validation...")
    
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    repo = Repository(filename=path)
    user_service = UserService(repo=repo)
    
    # Test invalid username
    try:
        user_service.create_user("", 25)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Empty username validation working")
    
    # Test invalid age
    try:
        user_service.create_user("Test", -5)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Negative age validation working")
    
    # Test invalid height
    try:
        user_service.create_user("Test", 25, height=-10)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Negative height validation working")
    
    os.unlink(path)
    print("✓ Input validation: PASSED\n")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("SPRINT 2 VALIDATION")
    print("=" * 60 + "\n")
    
    try:
        test_crud_operations()
        test_strategies()
        test_factory_pattern()
        test_scheduler()
        test_validation()
        
        print("=" * 60)
        print("ALL VALIDATION TESTS PASSED ✓")
        print("=" * 60)
        print("\nSprint 2 implementation is complete and functional!")
        print("- Full CRUD operations ✓")
        print("- Multiple strategy patterns ✓")
        print("- Factory pattern ✓")
        print("- Input validation ✓")
        print("- Exception handling ✓")
        return 0
        
    except Exception as e:
        print(f"\n✗ VALIDATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
