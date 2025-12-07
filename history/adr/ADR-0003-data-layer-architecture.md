# ADR-0003: Data Layer Architecture

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** 001-retro-todo-app
- **Context:** The application requires a data persistence strategy that supports offline-first operation, provides type safety, and meets <200ms latency requirements while handling up to 100k tasks.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects all data operations, model contracts
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - SQLite, shelve, YAML, dataclasses evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Models, database, services all depend on this -->

## Decision

Adopt a three-component data layer architecture:

| Component | Technology | Version | Responsibility |
|-----------|------------|---------|----------------|
| Data Models | Pydantic v2 | 2.0+ | Type validation, serialization, business constraints |
| Persistence | TinyDB | 4.8+ | Document storage, CRUD operations |
| Performance | CachingMiddleware | (bundled) | In-memory read caching |

### Pydantic v2 Configuration

**Model Definition Pattern:**
```python
from pydantic import BaseModel, field_validator

class TodoTask(BaseModel):
    id: int
    title: str
    # ... fields with strict type hints

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

**Mandatory Syntax (v2 only):**
- ✅ `@field_validator` decorator
- ✅ `@model_validator` decorator  
- ✅ `@classmethod` on all validators
- ❌ `@validator` (v1 syntax - PROHIBITED)
- ❌ `@root_validator` (v1 syntax - PROHIBITED)

### TinyDB Configuration

**Database Initialization:**
```python
from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage

db = TinyDB(
    'todo_data.json',
    storage=CachingMiddleware(JSONStorage),
    indent=2,
    ensure_ascii=False
)
```

**Performance Characteristics:**
| Operation | Latency (1000 tasks) | Cache Impact |
|-----------|---------------------|--------------|
| Read (single) | <10ms | 10x faster (cached) |
| List (all) | <50ms | 10x faster (cached) |
| Search/Filter | <100ms | 5x faster (cached) |
| Write | <50ms | 5% slower (invalidation) |

**ID Generation:**
- Atomic auto-increment using table metadata
- Prevents ID collisions in concurrent scenarios

## Consequences

### Positive

- **Type safety**: Pydantic catches validation errors at data boundary
- **Performance**: CachingMiddleware provides sub-200ms reads at scale
- **Offline-first**: No external database dependencies, single JSON file
- **Portability**: Database file can be copied/backed up trivially
- **Schema evolution**: Pydantic models support default values for migration
- **Developer experience**: Clear validation errors with field context

### Negative

- **Memory footprint**: Cache grows with task count (~50KB per 1000 tasks)
- **Concurrent writes**: Limited multi-process support (single-user target)
- **Query complexity**: No SQL joins or complex aggregations
- **Migration effort**: v1→v2 Pydantic migration requires validator rewrites

## Alternatives Considered

### Alternative A: SQLite + dataclasses

- **Pros**: SQL queries, better concurrent writes, proven scalability
- **Cons**: No runtime validation, manual schema migrations, heavier setup
- **Why rejected**: Overkill for single-user offline app, loses type safety benefits

### Alternative B: YAML + attrs

- **Pros**: Human-readable, simple persistence
- **Cons**: No caching, slow at scale, attrs less rich than Pydantic
- **Why rejected**: Performance concerns at target scale (100k tasks)

### Alternative C: shelve + Pydantic

- **Pros**: Python standard library, dict-like interface
- **Cons**: Platform-dependent binary format, no JSON export
- **Why rejected**: Portability concerns, debugging difficulty

### Alternative D: SQLModel (Pydantic + SQLAlchemy)

- **Pros**: Best of both worlds, SQL support, Pydantic validation
- **Cons**: Significant complexity increase, requires SQLAlchemy knowledge
- **Why rejected**: Over-engineered for Phase I requirements

## References

- Feature Spec: [specs/001-retro-todo-app/spec.md](../../specs/001-retro-todo-app/spec.md)
- Implementation Plan: [specs/001-retro-todo-app/plan.md](../../specs/001-retro-todo-app/plan.md)
- Research Evidence: [specs/001-retro-todo-app/research.md](../../specs/001-retro-todo-app/research.md) (Sections 3, 4)
- Data Model Spec: [specs/001-retro-todo-app/data-model.md](../../specs/001-retro-todo-app/data-model.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Principles IV, V)
