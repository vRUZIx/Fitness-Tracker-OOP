# Sprint 1 Plan — Fitness Tracker (OOP)

## 1. Selected idea and scope

Project: Fitness Tracker (object-oriented demo).

Scope (Sprint 1):
- Provide a minimal, working prototype that demonstrates core OOP principles and partial CRUD persistence.
- Core features: create/read users, workouts, exercises; schedule a workout; persist data to JSON.

Out of scope (Sprint 1): full UI, advanced querying, full frontend, production-grade DB.

## 2. Real-world entities and core classes

Core classes (minimum four):
- `User` — represents a user (username, age, height, weight). Responsible for user-specific data and simple helpers.
- `Workout` — represents a workout (name, duration) and summary methods.
- `Exercise` — represents an exercise (name, calories) and helper methods.
- `Repository` / `IRepository` — abstraction for persistence (CRUD). Current implementation: `Repository` (JSON file) implementing `IRepository`.

Additional classes:
- `Scheduler` — coordinates scheduling logic between `User` and `Workout`.
- `ObjectFactory` — Factory pattern for creating domain objects.

Relationships / responsibilities:
- `Workout` composes `Exercise` instances (a workout can contain many exercises).
- `Scheduler` is a controller/coordinator that does not persist data itself.
- `IRepository` provides the persistence interface; `Repository` implements JSON storage. This supports dependency inversion and allows adding a `SqliteRepository` later.

## 3. Design principles mapping

- SOLID:
  - Single Responsibility: each class has a narrow responsibility (models vs persistence vs scheduling).
  - Open/Closed: `IRepository` allows adding new persistence backends without changing consumers.
  - Liskov Substitution: repository implementations follow the `IRepository` contract.
  - Interface Segregation: consumers depend on the small `IRepository` API.
  - Dependency Inversion: higher-level modules (business logic) depend on `IRepository` abstraction.

- GRASP:
  - Creator: `ObjectFactory` creates domain objects.
  - Controller: `Scheduler` coordinates operations between domain objects.
  - Low Coupling / High Cohesion: classes keep a single focus and interact via small, well-defined APIs.

- CUPID: Code is Composable, Understandable, Predictable, Idiomatic, Domain-based.

## 4. Persistence & CRUD

- Storage: JSON file at project root (`data.json`). Implemented `create`, `read_all`, `read_by_id`, `update`, `delete`, `find_by_type`.
- Records are structured with stable IDs (UUID hex): `{ "id": <id>, "type": <type>, "data": {...} }`.

## 5. Tests and Deliverables

- Unit tests: pytest tests added for core models and repository CRUD.
- Deliverables for Sprint 1:
  - Runnable `src/main.py` demonstrating create/read and scheduling.
  - `docs/plan.md`, `docs/class_diagram.puml`, `docs/architecture.md` (this file complements those).
  - Tests in `tests/` passing under pytest.

## 6. Next steps (Sprint 1 remaining)

Priority:
1. Add documentation artifacts (class diagrams) — done in this sprint.
2. Add logging and richer exception handling across modules.
3. Extend `ObjectFactory` to instantiate objects from record data.
4. Add CLI (`argparse`) to `src/main.py` to demonstrate CRUD commands.
5. Add GitHub Actions CI to run tests on push.

---
Created: Sprint 1 planning doc for the Fitness Tracker OOP project.
