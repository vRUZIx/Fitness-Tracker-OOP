# Demo Steps — Complete CLI and Interactive Examples

This file contains comprehensive examples for using the Fitness Tracker application in both CLI and interactive modes.

## Prerequisites

Run commands from the repository root (where `src/` lives).
The project entrypoint is `src/main.py`. You can run it with `python src/main.py`.
IDs for created records are printed on creation and visible via the `list` command.

## Quick Start Demo

### 1) Run the default demo (no args)

```bash
python src/main.py
```

This runs the built-in demo: creates a sample user and workout, prints summaries, saves a `demo` record to `data.json`, and prints a default schedule string.

### 2) Start Interactive Mode

```bash
python src/main.py interactive
```

This launches the interactive menu with all CRUD operations available.

## CLI Examples - User Management

### Create a User

```bash
python src/main.py create-user --username alice --age 30 --height 170 --weight 65
```

Example output:
```
Created user id=abc123def456
```

### Update a User

```bash
# Update all fields
python src/main.py update-user --id abc123def456 --username "Alice Smith" --age 31 --height 171 --weight 64

# Update specific fields only
python src/main.py update-user --id abc123def456 --age 32
```

### Delete a User

```bash
python src/main.py delete-user --id abc123def456
```

### List All Users

```bash
python src/main.py list-users
```

## CLI Examples - Workout Management

### Create a Workout

```bash
python src/main.py create-workout --name "Leg Day" --duration 45
```

### Update a Workout

```bash
# Update all fields
python src/main.py update-workout --id xyz789ghi012 --name "Upper Body" --duration 50

# Update specific fields only
python src/main.py update-workout --id xyz789ghi012 --duration 60
```

### Delete a Workout

```bash
python src/main.py delete-workout --id xyz789ghi012
```

### List All Workouts

```bash
python src/main.py list-workouts
```

## CLI Examples - General Operations

### List All Records

```bash
python src/main.py list
```

The `list` command prints all records saved in `data.json`. Use the `id` field shown to target `get`, `update`, `delete`, and `schedule` operations.

### Get a Single Record

```bash
python src/main.py get --id <record_id>
```

This displays the full record details plus any domain-specific information (e.g., user info, workout summary).

## CLI Examples - Workout Scheduling

### Schedule Workout (No Calorie Estimation)

```bash
python src/main.py schedule --user-id <user_id> --workout-id <workout_id>
```

### Schedule with Simple Calorie Strategy

```bash
python src/main.py schedule --user-id <user_id> --workout-id <workout_id> --strategy simple --met 5.0
```

### Schedule with Constant Burn Strategy

```bash
python src/main.py schedule --user-id <user_id> --workout-id <workout_id> --strategy constant --rate-per-min 4.0
```

Example output:
```
alice scheduled: Leg Day. Estimated calories: 225.0 kcal
```

## Complete Demonstration Workflow

```bash
# Create user
python src/main.py create-user --username "Alice" --age 30 --height 170 --weight 65

# Create workout
python src/main.py create-workout --name "Cardio Session" --duration 45

# List to get IDs
python src/main.py list

# Schedule with calories
python src/main.py schedule --user-id <user_id> --workout-id <workout_id> --strategy simple --met 6.0

# Update user
python src/main.py update-user --id <user_id> --weight 63

# Delete workout
python src/main.py delete-workout --id <workout_id>
```

## Tips

- Run tests with `pytest tests/` to avoid modifying `data.json`
- Use interactive mode for exploration: `python src/main.py interactive`
- Backup `data.json` before running demonstrations
- Reset data by removing or emptying `data.json`
