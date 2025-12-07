# Technical Documentation

## System Architecture

### Overview
The Fitness Tracker is a Python-based application that implements a layered architecture with clear separation of concerns. The system follows object-oriented design principles (SOLID, GRASP, CUPID) and employs multiple design patterns for flexibility and maintainability.

### Architecture Layers

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  (CLI Interface + Interactive Menu)     │
├─────────────────────────────────────────┤
│         Service Layer                   │
│  (UserService, WorkoutService)          │
├─────────────────────────────────────────┤
│         Domain Layer                    │
│  (User, Workout, Exercise Models)       │
├─────────────────────────────────────────┤
│         Data Access Layer               │
│  (Repository Pattern)                   │
├─────────────────────────────────────────┤
│         Persistence Layer               │
│  (JSON File Storage)                    │
└─────────────────────────────────────────┘
```

## Design Patterns

### 1. Factory Pattern
**Location**: `src/models/factory.py`

**Purpose**: Creates domain objects without exposing instantiation logic

**Implementation**:
```python
class ObjectFactory:
    @staticmethod
    def create_object(object_type, *args, **kwargs):
        if object_type == "user":
            return User(*args, **kwargs)
        elif object_type == "workout":
            return Workout(*args, **kwargs)
        # ...
```

**Benefits**:
- Single Responsibility: Object creation is centralized
- Open/Closed: Easy to add new object types
- Dependency Inversion: Clients depend on abstractions

### 2. Repository Pattern
**Location**: `src/repository/repository.py`

**Purpose**: Abstracts data persistence and provides a collection-like interface

**Implementation**:
- Interface: `IRepository` defines the contract
- Concrete: `Repository` implements JSON file persistence

**CRUD Operations**:
- Create: `create(item_dict, type_)`
- Read: `read_by_id(record_id)`, `read_all()`, `find_by_type(type_)`
- Update: `update(record_id, new_data)`
- Delete: `delete(record_id)`

**Benefits**:
- Information Expert (GRASP): Repository knows about data access
- Low Coupling: Services don't depend on storage implementation
- Single Responsibility: Data access logic is isolated

### 3. Strategy Pattern
**Location**: `src/strategies/`

**Purpose**: Encapsulates interchangeable algorithms for calculations

#### Calorie Strategies
- `CalorieStrategy` (Abstract Base)
- `SimpleCalorieStrategy`: MET-based calculation
- `ConstantBurnStrategy`: Fixed rate calculation

#### Intensity Strategies
- `IntensityStrategy` (Abstract Base)
- `AgeBasedIntensityStrategy`: Age and duration based
- `DurationBasedIntensityStrategy`: Duration only based

**Benefits**:
- Open/Closed: New strategies can be added without modifying existing code
- Polymorphism: Runtime algorithm selection
- Protected Variations (GRASP): Changes to algorithms don't affect clients

### 4. Service Layer Pattern
**Location**: `src/services/`

**Purpose**: Encapsulates business logic and orchestrates operations

**Services**:
- `UserService`: User management operations
- `WorkoutService`: Workout management operations
- `Scheduler`: Workout scheduling with strategy integration

**Benefits**:
- Controller (GRASP): Coordinates system operations
- High Cohesion: Each service handles related operations
- Single Responsibility: Business logic separated from presentation

## SOLID Principles Application

### Single Responsibility Principle (SRP)
Each class has one reason to change:
- `User`: Represents user data
- `UserService`: Manages user operations
- `Repository`: Handles data persistence
- `CalorieStrategy`: Calculates calories
- `main.py`: Provides CLI interface

### Open/Closed Principle (OCP)
System is open for extension, closed for modification:
- New strategies can be added without changing `Scheduler`
- New object types can be added to `ObjectFactory`
- New services can be added without modifying existing ones

### Liskov Substitution Principle (LSP)
Derived classes are substitutable for base classes:
- All `CalorieStrategy` implementations can replace the base
- All `IntensityStrategy` implementations are interchangeable
- Repository implementations follow `IRepository` contract

### Interface Segregation Principle (ISP)
Clients depend only on interfaces they use:
- `IRepository` provides minimal required methods
- Strategy interfaces define single `calculate` method
- Services expose only relevant operations

### Dependency Inversion Principle (DIP)
High-level modules depend on abstractions:
- Services depend on `Repository` interface, not concrete implementation
- `Scheduler` depends on `CalorieStrategy` abstraction
- Factory creates objects based on type strings, not concrete classes

## GRASP Principles Application

### Information Expert
Responsibility assigned to class with necessary information:
- `User` provides user information through `get_info()`
- `Workout` provides workout summary through `get_summary()`
- `Repository` manages data access because it knows storage details

### Creator
Class responsible for creating objects:
- `ObjectFactory` creates domain objects
- `Repository` creates record structures
- Services create objects through factory

### Controller
Handles system events and coordinates operations:
- `UserService` and `WorkoutService` control business operations
- `Scheduler` coordinates workout scheduling
- CLI functions in `main.py` handle user commands

### Low Coupling
Dependencies between classes are minimized:
- Services depend on repository interface, not implementation
- Strategies are independent of each other
- Models have no dependencies on services or repository

### High Cohesion
Related functionality is grouped together:
- All user operations in `UserService`
- All workout operations in `WorkoutService`
- All persistence logic in `Repository`

### Protected Variations
Stable interfaces protect against changes:
- `IRepository` interface protects against storage changes
- Strategy pattern protects against algorithm changes
- Service layer protects business logic from presentation changes

## CUPID Principles Application

### Composable
Components can be combined easily:
- Services can be composed for complex operations
- Strategies can be combined in scheduling
- Repository can be injected into multiple services

### Unix Philosophy
Each component does one thing well:
- Models represent data
- Services handle operations
- Repository manages persistence
- Strategies perform calculations

### Predictable
Consistent behavior across components:
- All services follow same patterns
- CRUD operations work uniformly
- Strategies have consistent interfaces

### Idiomatic
Follows Python conventions:
- Duck typing where appropriate
- Properties and methods follow Python naming
- Exception handling uses Python patterns
- Docstrings document all public APIs

### Domain-based
Code reflects business domain:
- `User`, `Workout`, `Exercise` match domain concepts
- Service names reflect business operations
- Strategy names describe business algorithms

## Exception Handling and Logging

### Exception Hierarchy
```
Exception
├── ValueError (validation errors)
└── Generic exceptions (system errors)
```

### Logging Strategy
**Configuration**: `src/logging_config.py`

**Levels Used**:
- `INFO`: Successful operations (create, update, delete)
- `DEBUG`: Detailed operation information
- `ERROR`: Validation errors
- `EXCEPTION`: System errors with stack traces

**Log Points**:
- All service operations (create, update, delete)
- Repository operations (CRUD)
- Strategy calculations
- CLI operations

### Validation
All services validate inputs before processing:
- Type checking (isinstance)
- Value range checking (positive numbers)
- Required field checking (non-empty strings)
- Record existence checking (update/delete operations)

## Data Model

### Record Structure
```json
{
    "id": "unique_identifier",
    "type": "user|workout|exercise",
    "data": {
        // Type-specific fields
    }
}
```

### User Data
```json
{
    "username": "string",
    "age": "integer (positive)",
    "height": "float (optional, positive)",
    "weight": "float (optional, positive)"
}
```

### Workout Data
```json
{
    "name": "string",
    "duration": "integer (minutes, positive)"
}
```

## Testing Strategy

### Test Coverage
Target: 80%+ code coverage

### Test Types
1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Component interaction testing
3. **Edge Case Tests**: Boundary conditions and error scenarios
4. **Strategy Tests**: Algorithm verification

### Test Files
- `test_crud_operations.py`: Complete CRUD testing
- `test_intensity_strategy.py`: Intensity calculation tests
- `test_repository_extended.py`: Repository edge cases
- `test_calorie_strategy.py`: Calorie calculation tests
- `test_models.py`: Domain model tests
- `test_main_cli.py`: CLI functionality tests

### Test Fixtures
- `temp_repo`: Creates temporary JSON file for isolated testing
- `conftest.py`: Shared test configuration

## Extension Points

### Adding New Strategies
1. Create new class inheriting from `CalorieStrategy` or `IntensityStrategy`
2. Implement required abstract methods
3. Register in strategy factory function if needed

### Adding New Models
1. Create model class in `src/models/`
2. Add to `ObjectFactory.create_object()`
3. Add to `ObjectFactory.create_from_record()`
4. Create corresponding service if needed

### Adding New Services
1. Create service class in `src/services/`
2. Inject repository dependency
3. Implement business operations
4. Add CLI commands in `main.py`

## Performance Considerations

### Data Access
- In-memory operations after initial file read
- Batch writes to minimize I/O
- Unique ID generation using UUID4

### Scalability
- Current design suitable for small to medium datasets
- For large datasets, consider:
  - Database backend (extend `IRepository`)
  - Caching layer
  - Pagination in list operations

### Optimization Opportunities
- Lazy loading of records
- Index structures for faster lookups
- Connection pooling for future database integration

## Security Considerations

### Input Validation
- All user inputs validated before processing
- Type checking prevents type confusion attacks
- Range checking prevents invalid data

### Data Integrity
- Atomic file writes
- Validation before persistence
- Type enforcement in models

### Future Enhancements
- User authentication
- Access control
- Encrypted data storage
- Audit logging

## Deployment

### Requirements
- Python 3.8+
- Dependencies in `requirements.txt`
- Write permissions for data directory

### Configuration
- Data file location configurable in `Repository.__init__()`
- Logging configuration in `logging_config.py`
- Default values in services

### Maintenance
- Regular backups of `data.json`
- Log rotation recommended for production
- Periodic cleanup of old records
