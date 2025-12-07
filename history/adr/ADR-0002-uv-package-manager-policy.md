# ADR-0002: UV Package Manager Policy

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** 001-retro-todo-app
- **Context:** The project requires a package manager that provides fast, reproducible builds and eliminates common dependency hell issues experienced with pip and other Python package managers.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects all developers, CI/CD, onboarding
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - pip, poetry, pipenv, pdm evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Development workflow, deployment, documentation -->

## Decision

Adopt **uv** as the exclusive package manager for all dependency operations. This is a **NON-NEGOTIABLE** constitutional principle.

**Permitted Commands:**
| Operation | Command |
|-----------|---------|
| Initialize project | `uv init` |
| Add dependency | `uv add <package>` |
| Add dev dependency | `uv add --dev <package>` |
| Sync environment | `uv sync` |
| Run commands | `uv run <command>` |
| Update dependencies | `uv lock --upgrade` |

**Prohibited Tools:**
- ❌ pip (no `pip install`)
- ❌ poetry (no `poetry add`)
- ❌ pipenv (no `pipenv install`)
- ❌ pdm (no `pdm add`)
- ❌ conda (no `conda install`)

**Lock File Policy:**
- `uv.lock` MUST be committed to version control
- Lock file ensures reproducible builds across all environments
- CI must run `uv sync` to restore exact dependency versions

## Consequences

### Positive

- **10-100x faster**: uv is written in Rust, dramatically faster than pip/poetry
- **Reproducible builds**: Lock file guarantees identical environments
- **Single source of truth**: `pyproject.toml` + `uv.lock` define complete dependency graph
- **Modern resolver**: Handles complex dependency trees without conflicts
- **Drop-in replacement**: Compatible with pyproject.toml standard

### Negative

- **Team adoption**: Developers must learn new tool (low barrier, similar commands)
- **Ecosystem maturity**: uv is newer than pip/poetry (rapidly maturing)
- **IDE integration**: Some IDEs may not auto-detect uv environments
- **Documentation lag**: Some guides still reference pip commands

## Alternatives Considered

### Alternative A: pip + requirements.txt

- **Pros**: Universal familiarity, zero learning curve
- **Cons**: Slow, no lock file, manual version pinning, frequent conflicts
- **Why rejected**: Does not meet reproducibility or speed requirements

### Alternative B: Poetry

- **Pros**: Excellent dependency resolution, mature ecosystem
- **Cons**: 10-50x slower than uv, heavy virtual environment management
- **Why rejected**: Performance penalty unacceptable for development velocity

### Alternative C: pipenv

- **Pros**: Combines pip and virtualenv, Pipfile.lock
- **Cons**: Known performance issues, maintenance concerns, complex internals
- **Why rejected**: Reliability and speed concerns documented in community

### Alternative D: PDM

- **Pros**: PEP 582 support, modern resolver
- **Cons**: Less adoption than poetry, limited tooling integration
- **Why rejected**: Smaller community, less battle-tested

## References

- Feature Spec: [specs/001-retro-todo-app/spec.md](../../specs/001-retro-todo-app/spec.md)
- Implementation Plan: [specs/001-retro-todo-app/plan.md](../../specs/001-retro-todo-app/plan.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Principle II)
- uv Documentation: https://docs.astral.sh/uv/
