# Fitness Tracker - User Guide

## Table of Contents
1. [Installation](#installation)
2. [Running the Application](#running-the-application)
3. [Command-Line Interface](#command-line-interface)
4. [Interactive Menu Mode](#interactive-menu-mode)
5. [CRUD Operations](#crud-operations)
6. [Testing](#testing)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. Clone or download the project to your local machine

2. Navigate to the project directory:
```bash
cd FitnessTrackerOOPESAS
```

3. Create and activate a conda environment (recommended):
```bash
conda create -n fitness-tracker python=3.9
conda activate fitness-tracker
```

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Default Demo Mode
Run the application without arguments to see a quick demonstration:
```bash
python src/main.py
```

### Interactive Menu Mode
Start the interactive menu for full functionality:
```bash
python src/main.py interactive
```

### Command-Line Interface
Use specific commands for direct operations (see [CLI section](#command-line-interface))

## Command-Line Interface

The Fitness Tracker provides a comprehensive CLI for all operations:

### User Management

#### Create User
```bash
python src/main.py create-user --username "John Doe" --age 30 --height 175.5 --weight 70.0
```

#### Update User
```bash
python src/main.py update-user --id <user_id> --username "Jane Doe" --age 31
```

#### Delete User
```bash
python src/main.py delete-user --id <user_id>
```

#### List All Users
```bash
python src/main.py list-users
```

### Workout Management

#### Create Workout
```bash
python src/main.py create-workout --name "Morning Run" --duration 30
```

#### Update Workout
```bash
python src/main.py update-workout --id <workout_id> --name "Evening Run" --duration 45
```

#### Delete Workout
```bash
python src/main.py delete-workout --id <workout_id>
```

#### List All Workouts
```bash
python src/main.py list-workouts
```

### General Operations

#### List All Records
```bash
python src/main.py list
```

#### Get Specific Record
```bash
python src/main.py get --id <record_id>
```

#### Schedule Workout
```bash
# Basic scheduling
python src/main.py schedule --user-id <user_id> --workout-id <workout_id>

# With simple calorie strategy
python src/main.py schedule --user-id <user_id> --workout-id <workout_id> --strategy simple --met 6.0

# With constant burn strategy
python src/main.py schedule --user-id <user_id> --workout-id <workout_id> --strategy constant --rate-per-min 5.0
```

## Interactive Menu Mode

The interactive menu provides a user-friendly interface for all operations:

```bash
python src/main.py interactive
```

### Menu Options

1. **Create user** - Add a new user with personal details
2. **Create workout** - Add a new workout with name and duration
3. **List all records** - Display all users and workouts
4. **Get record by ID** - View details of a specific record
5. **Update user** - Modify existing user information
6. **Update workout** - Modify existing workout details
7. **Delete user** - Remove a user from the system
8. **Delete workout** - Remove a workout from the system
9. **List users only** - Display only user records
10. **List workouts only** - Display only workout records
11. **Schedule workout** - Assign a workout to a user with calorie calculation
12. **History** - View recent actions
13. **Exit** - Close the application

### Interactive Mode Features

- **Input validation**: The system validates all inputs in real-time
- **Confirmation prompts**: Critical operations (delete, create) require confirmation
- **Default values**: Current values are shown when updating records
- **Error handling**: Clear error messages for invalid operations
- **History tracking**: View your recent actions

## CRUD Operations

### Create Operations

**Users**: Create with username, age, and optional height/weight
```python
# Example output
Created user id=abc123def456
```

**Workouts**: Create with name and duration in minutes
```python
# Example output
Created workout id=xyz789ghi012
```

### Read Operations

**Single Record**: Retrieve by ID
```python
# Returns record details with type and data
{'id': 'abc123', 'type': 'user', 'data': {'username': 'John', 'age': 30}}
```

**List All**: Get all records or filtered by type
```python
# Users only
Total users: 5

# Workouts only
Total workouts: 3
```

### Update Operations

**Partial Updates**: Update only specific fields
```bash
# Update only age
python src/main.py update-user --id <user_id> --age 32

# Update only workout duration
python src/main.py update-workout --id <workout_id> --duration 45
```

**Full Updates**: Update all fields
```bash
python src/main.py update-user --id <user_id> --username "New Name" --age 35 --height 180 --weight 75
```

### Delete Operations

**Safe Deletion**: System validates record type before deletion
```bash
python src/main.py delete-user --id <user_id>
# Output: Deleted user id=<user_id>
```

## Testing

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test Files
```bash
# Test CRUD operations
pytest tests/test_crud_operations.py

# Test strategies
pytest tests/test_intensity_strategy.py
pytest tests/test_calorie_strategy.py

# Test repository
pytest tests/test_repository_extended.py
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: Service and repository interaction
- **Edge Case Tests**: Boundary conditions and error scenarios
- **Strategy Pattern Tests**: Calorie and intensity calculation strategies

## Data Persistence

All data is stored in `data.json` at the project root. The file uses JSON format:

```json
[
    {
        "id": "unique_id_1",
        "type": "user",
        "data": {
            "username": "John Doe",
            "age": 30,
            "height": 175.5,
            "weight": 70.0
        }
    },
    {
        "id": "unique_id_2",
        "type": "workout",
        "data": {
            "name": "Morning Run",
            "duration": 30
        }
    }
]
```

## Troubleshooting

### Common Issues

**Issue**: Module not found errors
**Solution**: Ensure you're in the project root and dependencies are installed

**Issue**: Data not persisting
**Solution**: Check write permissions for `data.json` file

**Issue**: Invalid ID errors
**Solution**: Use `list` or `list-users`/`list-workouts` to find valid IDs

**Issue**: Validation errors
**Solution**: Ensure all required fields meet validation criteria:
- Username: Non-empty string
- Age: Positive integer
- Height/Weight: Positive numbers
- Duration: Positive integer

## Best Practices

1. **Always validate IDs** before update/delete operations using list commands
2. **Use interactive mode** for exploratory operations
3. **Use CLI commands** for scripting and automation
4. **Regular backups** of `data.json` recommended
5. **Check logs** in case of errors for detailed information

## Support

For additional help:
- Check `docs/demo_steps.md` for demonstration scenarios
- Review `docs/architecture.md` for system design details
- Examine test files for usage examples
