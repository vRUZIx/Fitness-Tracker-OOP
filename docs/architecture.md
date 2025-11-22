# Architecture Notes — Sprint 1

This file explains how the codebase applies OOP principles and design patterns.

## Design patterns used

- Factory: `ObjectFactory` centralizes object creation and keeps construction logic out of business classes.
- Repository: `IRepository` + `Repository` implement a persistence abstraction (dependency inversion).

## SOLID / GRASP / CUPID mapping

- **Single Responsibility**: models (`User`, `Workout`, `Exercise`) handle domain data; `Repository` handles persistence; `Scheduler` handles coordination.
- **Open/Closed**: new repository implementations can be added by implementing `IRepository`.
- **Liskov Substitution**: `Repository` implements `IRepository` and can be swapped with another implementation.
- **Interface Segregation**: the repository interface is small and focused.
- **Dependency Inversion**: higher-level code depends on `IRepository` abstractions.

GRASP principles applied:
- Creator: `ObjectFactory` acts as a creator for domain objects.
- Controller: `Scheduler` orchestrates behavior.

CUPID: Code is kept idiomatic and domain-focused; classes are small and composable.

## Persistence

Records use structured JSON with stable IDs. This simplifies update/delete operations and enables future migration to relational storage (SQLite) without changing business logic.

## Logging & Error Handling (next step)

Add a `logging` configuration (module-level) and add informative `logger.info()` / `logger.exception()` calls around repository I/O and scheduling actions.
