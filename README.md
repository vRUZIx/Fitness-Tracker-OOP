# Fitness Tracker (OOP) - Sprint 2 Complete

![CI](https://github.com/vRUZIx/Fitness-Tracker-OOP/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/vRUZIx/Fitness-Tracker-OOP/branch/sprint1/graph/badge.svg)](https://codecov.io/gh/vRUZIx/Fitness-Tracker-OOP)

A comprehensive object-oriented fitness tracker application demonstrating SOLID, GRASP, and CUPID principles with full CRUD operations, multiple design patterns, and extensive test coverage.

## Features

### Complete CRUD Operations
- **Create**: Users and workouts with validation
- **Read**: Single records, all records, filtered by type
- **Update**: Partial or full updates with validation
- **Delete**: Safe deletion with type checking

### Design Patterns
- **Factory Pattern**: Centralized object creation
- **Repository Pattern**: Abstracted data persistence
- **Strategy Pattern**: Pluggable calorie and intensity calculations
- **Service Layer Pattern**: Business logic orchestration

### User Interface
- **CLI Commands**: Direct command-line operations for automation
- **Interactive Menu**: User-friendly menu-driven interface with 13 options
- **Input Validation**: Real-time validation with helpful error messages
- **Confirmation Prompts**: Safe operations with user confirmation

### Advanced Features
- Multiple calorie calculation strategies (MET-based, constant rate)
- Intensity calculation strategies (age-based, duration-based)
- Comprehensive logging and exception handling
- JSON-based data persistence
- 80%+ test coverage

## Project Structure

```
FitnessTrackerOOPESAS/
├── src/
│   ├── main.py                 # CLI interface and interactive menu
│   ├── logging_config.py       # Logging configuration
│   ├── models/
│   │   ├── user.py            # User domain model
│   │   ├── workout.py         # Workout domain model
│   │   ├── exercise.py        # Exercise domain model
│   │   └── factory.py         # Factory pattern implementation
│   ├── repository/
│   │   ├── irepository.py     # Repository interface
│   │   └── repository.py      # JSON repository implementation
│   ├── services/
│   │   ├── user_service.py    # User management service
│   │   ├── workout_service.py # Workout management service
│   │   └── scheduler.py       # Workout scheduling service
│   └── strategies/
│       ├── calorie_strategy.py    # Calorie calculation strategies
│       └── intensity_strategy.py  # Intensity calculation strategies
├── tests/
│   ├── test_crud_operations.py      # CRUD operation tests
│   ├── test_intensity_strategy.py   # Intensity strategy tests
│   ├── test_repository_extended.py  # Repository edge case tests
│   └── [other test files]
├── docs/
│   ├── user_guide.md               # Complete user documentation
│   ├── technical_documentation.md  # Architecture and design details
│   ├── demo_steps.md               # Demo scenarios and examples
│   └── [other documentation]
└── data.json                        # Persistent data storage
```

## Quick Start

### Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:

```powershell
pip install -r requirements.txt
```

### Run the Application

**Default Demo**:
```powershell
python src/main.py
```

**Interactive Menu**:
```powershell
python src/main.py interactive
```

**CLI Commands**:
```powershell
# Create user
python src/main.py create-user --username "John" --age 30 --height 180 --weight 75

# Create workout
python src/main.py create-workout --name "Morning Run" --duration 30

# List all users
python src/main.py list-users

# Update user
python src/main.py update-user --id <user_id> --age 31

# Delete workout
python src/main.py delete-workout --id <workout_id>

# Schedule workout with calorie estimation
python src/main.py schedule --user-id <user_id> --workout-id <workout_id> --strategy simple --met 6.0
```

See `docs/user_guide.md` for complete command reference.

## Testing

**Run all tests**:
```powershell
python -m pytest tests/
```

**Run with coverage**:
```powershell
python -m pytest --cov=src --cov-report=html
python -m pytest --cov=src --cov-report=xml:coverage.xml
```

**Run specific test categories**:
```powershell
pytest tests/test_crud_operations.py -v
pytest tests/test_intensity_strategy.py -v
```

## Documentation

- **[User Guide](docs/user_guide.md)**: Complete usage instructions
- **[Technical Documentation](docs/technical_documentation.md)**: Architecture and design patterns
- **[Demo Steps](docs/demo_steps.md)**: Example scenarios and workflows
- **[Architecture](docs/architecture.md)**: System design overview
- **[Class Diagram](docs/class_diagram.puml)**: UML class diagram

## Design Principles Applied

### SOLID
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Extensible without modification (Strategy pattern)
- **Liskov Substitution**: Strategies are interchangeable
- **Interface Segregation**: Minimal interfaces (IRepository)
- **Dependency Inversion**: Services depend on abstractions

### GRASP
- **Information Expert**: Responsibilities assigned to classes with needed information
- **Creator**: Factory creates objects
- **Controller**: Services coordinate operations
- **Low Coupling**: Minimal dependencies between components
- **High Cohesion**: Related functionality grouped together

### CUPID
- **Composable**: Components combine easily
- **Unix Philosophy**: Each component does one thing well
- **Predictable**: Consistent behavior across components
- **Idiomatic**: Follows Python conventions
- **Domain-based**: Code reflects business domain

## Sprint 2 Enhancements

✅ Complete CRUD operations (Update and Delete)
✅ Enhanced modularity with service layer pattern
✅ Multiple strategy pattern implementations
✅ Interactive CLI menu interface
✅ Comprehensive exception handling and logging
✅ 80%+ test coverage with edge cases
✅ Complete technical and user documentation
✅ Integration testing and validation

## CI/CD

The GitHub Actions workflow:
- Runs all tests on push/pull request
- Generates coverage reports
- Produces coverage XML as workflow artifact
- Supports Codecov integration

To produce an HTML report locally:

```powershell
python -m pytest --cov=src --cov-report=xml:coverage.xml --cov-report=html:coverage_html
```

The CI workflow now uploads the `coverage_html` directory as a workflow artifact so you can download and inspect the full HTML report from the GitHub Actions run.

## Notes and next steps

- `Repository` writes to `data.json` at the project root to avoid creating multiple files when running from different CWDs.
- You can extend models, add CLI options to `src/main.py`, or add CI (GitHub Actions) for automated tests.

## CLI Examples

Quick examples — see `docs/demo_steps.md` for more details.

Create a user:

```powershell
python src/main.py create-user --username alice --age 30 --height 170 --weight 65
```

Create a workout:

```powershell
python src/main.py create-workout --name "Leg Day" --duration 45
```

List records and get a single record:

```powershell
python src/main.py list
python src/main.py get --id <id>
```

Schedule a workout (no calorie estimation):

```powershell
python src/main.py schedule --user-id <user_id> --workout-id <workout_id>
```

Schedule with calorie estimation strategies:

```powershell
# MET-based simple strategy
python src/main.py schedule --user-id <user_id> --workout-id <workout_id> --strategy simple --met 5.0

# Constant calories-per-minute strategy
python src/main.py schedule --user-id <user_id> --workout-id <workout_id> --strategy constant --rate-per-min 4.0
```
