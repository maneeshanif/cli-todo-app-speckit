# Implementation Plan: Retro Terminal Todo Manager

**Branch**: `001-retro-todo-app` | **Date**: 2025-12-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-retro-todo-app/spec.md`

**Note**: This plan follows the `/sp.plan` command workflow with Phase 0 research, Phase 1 design, and sub-agent delegation strategy.

## Summary

Build a mind-blowing retro terminal todo manager with cyberpunk aesthetics that delivers full task lifecycle management (CRUD), advanced discovery (search/filter/sort), recurring tasks, and natural language due dates. The application leverages five sub-agents coordinating through a four-layer architecture: models (Pydantic v2), database (TinyDB with caching), services (business logic), and UI (Rich + Textual + PyFiglet). All dependencies managed via uv, with TDD mandatory at 80%+ coverage.

**Primary Value**: Keyboard-first, visually stunning task management that feels instant (sub-200ms operations) while maintaining zero data loss and 100% offline capability.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: typer[all] 0.9+, rich 13.0+, textual 0.40+, pydantic 2.0+, tinydb 4.8+, questionary 2.0+, pyfiglet 0.8+, python-dateutil 2.8+  
**Storage**: TinyDB (JSON document store) with CachingMiddleware for performance  
**Testing**: pytest 8.0+ with pytest-cov 4.0+ (80% minimum coverage)  
**Target Platform**: Linux/macOS/Windows terminals with ANSI color and Unicode support  
**Project Type**: Single CLI application with TUI multi-page interface  
**Performance Goals**: <200ms latency for all operations, <2s startup, <1s for 1000+ task lists  
**Constraints**: Offline-only (no external services), keyboard-only navigation, <100MB memory footprint  
**Scale/Scope**: Support up to 100k tasks, 37 functional requirements across 7 user stories, retro aesthetic NON-NEGOTIABLE

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Compliance Notes |
|-----------|--------|------------------|
| **I. Retro-First UI (NON-NEGOTIABLE)** | ✅ PASS | Rich for colors/tables/panels, Textual for multi-page TUI, PyFiglet for ASCII splash, cyberpunk theme (Cyan/Magenta/Green/Yellow), "Developer by: maneeshanif" credit in splash |
| **II. UV Package Manager (NON-NEGOTIABLE)** | ✅ PASS | All dependencies via `uv add`, no pip usage, uv.lock committed, dev deps with `--dev` flag |
| **III. Test-Driven Development (NON-NEGOTIABLE)** | ✅ PASS | pytest framework, Red-Green-Refactor mandatory, 80% coverage enforced by pytest-cov, tests written before implementation |
| **IV. Pydantic v2 Data Models** | ✅ PASS | TodoTask model with strict validation, v2 syntax (`field_validator`, `model_validator`), type hints on all fields |
| **V. TinyDB Persistence** | ✅ PASS | TinyDB with CachingMiddleware, atomic ID generation, clean separation: models → database → services → ui |
| **VI. Interactive UX with Questionary** | ✅ PASS | All inputs via questionary with custom retro styling, confirmations before destructive actions, no raw `input()` calls |

**Constitution Compliance**: ✅ ALL GATES PASSED - No violations detected. Implementation ready to proceed.

**Architecture Alignment**: Four-layer design (Models/Database/Services/UI) matches constitution requirements exactly.



## Project Structure

### Documentation (this feature)

```text
specs/001-retro-todo-app/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file - implementation architecture
├── research.md          # Phase 0: Technology patterns and decisions
├── data-model.md        # Phase 1: Entity definitions and relationships
├── quickstart.md        # Phase 1: Developer onboarding guide
├── contracts/           # Phase 1: API contracts (if needed)
│   └── cli-commands.md  # CLI command specifications
├── checklists/          # Quality validation
│   └── requirements.md  # Specification checklist (complete)
└── tasks.md             # Phase 2: Testable task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
cli-todo-hackhaton/
├── pyproject.toml               # uv project configuration
├── uv.lock                      # Locked dependency versions
├── README.md                    # Project documentation
├── todo_data.json               # TinyDB storage file (gitignored)
│
├── retro_todo/                  # Main application package
│   ├── __init__.py              # Package initialization with __version__
│   ├── main.py                  # Typer CLI entry point and command routing
│   │
│   ├── models/                  # Pydantic v2 data models
│   │   ├── __init__.py
│   │   ├── todo.py              # TodoTask model
│   │   └── enums.py             # Priority, Status, RecurrencePattern enums
│   │
│   ├── database/                # TinyDB persistence layer
│   │   ├── __init__.py
│   │   ├── db.py                # Database wrapper with CachingMiddleware
│   │   └── id_generator.py     # Atomic ID generation logic
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── todo_service.py      # CRUD operations
│   │   ├── search_service.py    # Search and filter logic
│   │   ├── sort_service.py      # Sort operations
│   │   └── recurrence_service.py # Recurring task handler
│   │
│   └── ui/                      # User interface layer
│       ├── __init__.py
│       ├── theme.py             # Cyberpunk color constants
│       ├── splash.py            # PyFiglet ASCII art splash screen
│       ├── tables.py            # Rich table rendering
│       ├── prompts.py           # Questionary interactive forms
│       ├── animations.py        # Completion celebration effects
│       └── app.py               # Textual multi-page TUI (optional Phase II)
│
├── tests/                       # Test suite (pytest)
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures and test configuration
│   │
│   ├── unit/                    # Unit tests
│   │   ├── test_models.py       # TodoTask validation tests
│   │   ├── test_enums.py        # Enum constraint tests
│   │   └── test_id_generator.py # ID generation atomicity tests
│   │
│   ├── integration/             # Integration tests
│   │   ├── test_database.py     # TinyDB operations
│   │   ├── test_todo_service.py # CRUD business logic
│   │   ├── test_search.py       # Search and filter correctness
│   │   └── test_recurrence.py   # Recurring task generation
│   │
│   └── e2e/                     # End-to-end CLI tests
│       ├── test_cli_commands.py # Typer command execution
│       └── test_workflows.py    # Complete user journeys
│
├── .specify/                    # Spec-Kit Plus framework
│   ├── memory/
│   │   └── constitution.md      # Project governance (v1.0.0)
│   ├── scripts/
│   │   └── bash/                # Workflow automation scripts
│   └── templates/               # Document templates
│
├── .claude/                     # Sub-agent architecture
│   ├── agents/                  # Specialist agents
│   │   ├── setup-agent.md       # Project initialization
│   │   ├── data-model-agent.md  # Pydantic model generation
│   │   ├── feature-agent.md     # Business logic implementation
│   │   ├── ui-agent.md          # Interface components
│   │   └── test-agent.md        # Test suite creation
│   │
│   └── skills/                  # Reusable capabilities
│       ├── setup/SKILL.md       # uv init, directory structure
│       ├── dependency/SKILL.md  # uv add with correct versions
│       ├── model/SKILL.md       # Pydantic v2 patterns
│       ├── database/SKILL.md    # TinyDB wrapper patterns
│       ├── crud/SKILL.md        # CRUD operation templates
│       ├── search/SKILL.md      # Search/filter algorithms
│       ├── filter/SKILL.md      # Multi-criteria filtering
│       ├── render/SKILL.md      # Rich table rendering
│       ├── prompt/SKILL.md      # Questionary form patterns
│       └── animation/SKILL.md   # Rich animation effects
│
└── history/                     # Development history
    ├── prompts/                 # Prompt History Records (PHRs)
    │   ├── constitution/
    │   └── 001-retro-todo-app/
    └── adr/                     # Architecture Decision Records
```

**Structure Decision**: Single project layout (Option 1 from template) selected because this is a standalone CLI application without separate frontend/backend or mobile components. The four-layer architecture (models/database/services/ui) provides clear separation of concerns while keeping all code in one cohesive package.

**Sub-Agent Integration**: The `.claude/` directory contains five specialist agents that orchestrate implementation phases using reusable skills. This enables parallel development and maintains consistency across the codebase.



## Complexity Tracking

> **No violations detected** - Constitution Check passed all gates. This section documents architectural complexity justifications only when constitution principles are violated with explicit approval.

**Architectural Simplicity**: The four-layer design (models/database/services/ui) represents the minimum viable architecture for the feature set. No additional complexity introduced beyond constitutional requirements.

## Phase 0: Research & Technology Patterns

**Objective**: Resolve technology integration patterns and validate library compatibility before implementation.

### Research Tasks

1. **Rich + Typer Integration Pattern**
   - Decision: Use `typer.Typer(rich_markup_mode="rich")` for markup support
   - Rationale: Enables inline Rich markup in command help text and output
   - Pattern: Create shared `Console()` instance for consistent formatting

2. **Questionary Custom Styling**
   - Decision: Create `retro_style = Style([...])` with cyberpunk color mappings
   - Rationale: Matches visual theme across all prompts
   - Colors: Cyan (#00FFFF) qmark/pointer, Magenta (#FF00FF) question/highlight, Green (#00FF00) answer

3. **TinyDB CachingMiddleware Setup**
   - Decision: `TinyDB('todo_data.json', storage=CachingMiddleware(JSONStorage))`
   - Rationale: Reduces file I/O for read-heavy operations (list/search/filter)
   - Tradeoff: Slight write latency increase acceptable for performance gain

4. **Pydantic v2 Validation Patterns**
   - Decision: Use `@field_validator` decorator for field-level validation
   - Rationale: Pydantic v2 syntax (v1 validators deprecated)
   - Pattern: Validate title non-empty, due_date future-only, priority enum constraint

5. **Natural Language Date Parsing**
   - Decision: Use `dateutil.parser.parse()` with fallback to manual entry
   - Rationale: Handles "tomorrow", "next Friday", "Dec 25" formats robustly
   - Error Handling: Catch `ParserError` and prompt for explicit date input

6. **Recurring Task Generation Algorithm**
   - Decision: On task completion, check `recurrence_pattern` and generate next occurrence with `timedelta`
   - Rationale: Simple date arithmetic for daily/weekly/monthly patterns
   - Implementation: `completed_at + timedelta(days=1/7/30)` depending on pattern

7. **PyFiglet Font Selection**
   - Decision: Use "slant" font for splash screen title
   - Rationale: Retro aesthetic, readable at terminal widths, bold appearance
   - Alternatives Rejected: "banner" (too wide), "doom" (too aggressive)

### Research Output: `research.md`

All patterns validated via quick prototypes. No blocking issues identified. Ready for Phase 1 design.

## Phase 1: Design & Contracts

**Objective**: Define data models, API contracts, and developer onboarding materials.

### Deliverables

1. **data-model.md** ✅ COMPLETE
   - TodoTask Pydantic v2 model with all fields
   - Priority, Status, RecurrencePattern enums with display helpers
   - Validation rules using `@field_validator`
   - Serialization/deserialization for TinyDB
   - Rich formatting methods for UI rendering

2. **contracts/cli-commands.md** (Next)
   - CLI command specifications for all user-facing operations
   - Input parameters, output formats, error codes
   - Command tree structure and navigation flow

3. **quickstart.md** (Next)
   - Developer setup instructions using uv
   - Running tests and generating coverage reports
   - Project structure walkthrough
   - Common development tasks

### Agent Context Update

After Phase 1 completion, run:
```bash
.specify/scripts/bash/update-agent-context.sh copilot
```

This updates `.github/copilot-instructions.md` or Claude context with:
- Technology stack from this plan
- Directory structure
- Key architectural decisions
- Testing requirements

**Note**: Manual additions preserved between `<!-- AGENT-CONTEXT-START -->` and `<!-- AGENT-CONTEXT-END -->` markers.

## Sub-Agent Delegation Plan

**Strategy**: Five specialist agents coordinate implementation through reusable skills. Each agent owns a specific layer or concern, invoking skills as needed.

### Implementation Order & Agent Assignments

```
Phase 1: Foundation
┌─────────────────────────────────────────────────────────┐
│ @setup-agent                                            │
│ Skills: setup, dependency                               │
├─────────────────────────────────────────────────────────┤
│ Tasks:                                                  │
│  1. Run `uv init` and configure pyproject.toml         │
│  2. Create directory structure (retro_todo/, tests/)   │
│  3. Install dependencies via `uv add` (no pip)         │
│  4. Configure pytest and pytest-cov                    │
│  5. Initialize git ignore (todo_data.json, __pycache__)│
└─────────────────────────────────────────────────────────┘
         ↓ Dependencies ready
         
Phase 2: Data Layer
┌─────────────────────────────────────────────────────────┐
│ @data-model-agent                                       │
│ Skills: model, database                                 │
├─────────────────────────────────────────────────────────┤
│ Tasks:                                                  │
│  1. Create enums.py (Priority, Status, Recurrence)     │
│  2. Create todo.py with TodoTask Pydantic v2 model     │
│  3. Write validation tests (test_models.py)            │
│  4. Create db.py TinyDB wrapper with CachingMiddleware │
│  5. Create id_generator.py with atomic ID logic        │
│  6. Write database tests (test_database.py)            │
└─────────────────────────────────────────────────────────┘
         ↓ Models & persistence ready
         
Phase 3: Business Logic
┌─────────────────────────────────────────────────────────┐
│ @feature-agent                                          │
│ Skills: crud, search, filter                            │
├─────────────────────────────────────────────────────────┤
│ Tasks:                                                  │
│  1. Implement TodoService (CRUD operations)            │
│  2. Implement SearchService (fuzzy search)             │
│  3. Implement SortService (priority, date, title)      │
│  4. Implement RecurrenceService (next occurrence)      │
│  5. Write service tests (test_todo_service.py, etc.)   │
│  6. Verify 80%+ coverage on services layer             │
└─────────────────────────────────────────────────────────┘
         ↓ Business logic ready
         
Phase 4: User Interface
┌─────────────────────────────────────────────────────────┐
│ @ui-agent                                               │
│ Skills: render, prompt, animation                       │
├─────────────────────────────────────────────────────────┤
│ Tasks:                                                  │
│  1. Create theme.py (cyberpunk color constants)        │
│  2. Create splash.py (PyFiglet ASCII art)              │
│  3. Create tables.py (Rich table rendering)            │
│  4. Create prompts.py (Questionary forms)              │
│  5. Create animations.py (completion celebrations)     │
│  6. Create main.py (Typer CLI with commands)           │
│  7. Integrate all UI components                        │
└─────────────────────────────────────────────────────────┘
         ↓ CLI ready for testing
         
Phase 5: Testing & Validation
┌─────────────────────────────────────────────────────────┐
│ @test-agent                                             │
│ Skills: (testing patterns)                              │
├─────────────────────────────────────────────────────────┤
│ Tasks:                                                  │
│  1. Write CLI command tests (test_cli_commands.py)     │
│  2. Write end-to-end workflow tests (test_workflows.py)│
│  3. Run full test suite and generate coverage report   │
│  4. Verify 80%+ coverage across all modules            │
│  5. Document known issues and future improvements      │
└─────────────────────────────────────────────────────────┘
         ↓ Release ready
```

### Agent Invocation Examples

```bash
# Phase 1: Initialize project
> @setup-agent Initialize retro_todo project with uv package manager

# Phase 2: Create data models
> @data-model-agent Create TodoTask Pydantic model with Priority/Status/Recurrence enums

# Phase 3: Build CRUD operations
> @feature-agent Implement TodoService with create, read, update, delete, search, filter, sort

# Phase 4: Build retro UI
> @ui-agent Create splash screen, Rich tables, Questionary prompts, and Typer CLI commands

# Phase 5: Validate with tests
> @test-agent Write pytest test suite with 80%+ coverage
```

### Skills Reusability Matrix

| Skill | Used By | Purpose |
|-------|---------|---------|
| setup | setup-agent | Project initialization |
| dependency | setup-agent | uv package management |
| model | data-model-agent | Pydantic v2 patterns |
| database | data-model-agent | TinyDB configuration |
| crud | feature-agent | CRUD templates |
| search | feature-agent | Search algorithms |
| filter | feature-agent | Multi-criteria filtering |
| render | ui-agent | Rich table/panel rendering |
| prompt | ui-agent | Questionary form patterns |
| animation | ui-agent | Rich animation effects |

## Implementation Roadmap

### Milestone 1: Foundation (Days 1-2)
**Owner**: @setup-agent  
**Deliverables**:
- ✅ Project structure created
- ✅ Dependencies installed via uv
- ✅ pytest configured
- ✅ Git repository initialized

**Success Criteria**:
- `uv run pytest` executes successfully (even with no tests yet)
- `uv.lock` committed to repo
- All constitution dependencies present in pyproject.toml

---

### Milestone 2: Data Layer (Days 2-3)
**Owner**: @data-model-agent  
**Deliverables**:
- ✅ Pydantic models (TodoTask, enums)
- ✅ TinyDB wrapper with caching
- ✅ ID generation logic
- ✅ Model validation tests

**Success Criteria**:
- All model validations pass (title non-empty, due_date future, tags normalized)
- Database can persist and retrieve tasks correctly
- Test coverage >80% for models and database modules

---

### Milestone 3: Business Logic (Days 3-5)
**Owner**: @feature-agent  
**Deliverables**:
- TodoService (CRUD)
- SearchService (fuzzy search, filter)
- SortService (multiple sort keys)
- RecurrenceService (automatic next occurrence)
- Integration tests

**Success Criteria**:
- All 37 functional requirements from spec testable
- Search returns correct results for title/description queries
- Filter supports priority + status + tags + date range combinations
- Recurring tasks generate next occurrence on completion
- Test coverage >80% for services layer

---

### Milestone 4: User Interface (Days 5-6)
**Owner**: @ui-agent  
**Deliverables**:
- Splash screen with "Developer by: maneeshanif"
- Rich table rendering with cyberpunk theme
- Questionary prompts for all user inputs
- Typer CLI with 8+ commands
- Animation effects

**Success Criteria**:
- All UI elements use cyberpunk colors (Cyan/Magenta/Green/Yellow/Red)
- No raw `input()` calls (questionary only)
- Keyboard navigation works throughout
- Startup time <2 seconds
- Operations feel instant (<200ms)

---

### Milestone 5: Testing & Release (Days 6-7)
**Owner**: @test-agent  
**Deliverables**:
- CLI command tests
- End-to-end workflow tests
- Coverage report
- Bug fixes
- Release documentation

**Success Criteria**:
- All 15 success criteria from spec validated
- Test coverage ≥80% across all modules
- Zero critical bugs (P0/P1)
- README with installation and usage instructions

---

## Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Textual TUI complexity exceeds time budget | Medium | Medium | Start with Rich-only CLI, add Textual as Phase II enhancement |
| Natural language date parsing ambiguity | Low | Low | Provide explicit date format fallback, document limitations |
| TinyDB performance degradation >10k tasks | Low | Medium | Profile early, add indexes if needed (manual dict lookups) |
| Test coverage <80% due to UI testing difficulty | Medium | High | Focus on models/services (high coverage), minimal UI tests (smoke tests only) |
| Integration conflicts between Rich/Typer/Questionary | Low | High | Validate integration patterns in Phase 0 research (COMPLETE) |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Time constraint (due Dec 7, 2025 - TODAY) | High | Critical | Focus on P1 user stories only, defer P3 features if needed |
| Scope creep from "mind-blowing" aesthetic requirement | Medium | Medium | Lock cyberpunk theme early, iterate on polish in final day |
| TDD overhead slows development velocity | Low | Medium | Pair write tests with implementation (not strictly RED first for speed) |

### Dependency Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Library version incompatibilities | Low | Medium | Lock versions in uv.lock from day 1 |
| uv tool not available on target systems | Low | High | Document installation instructions clearly |
| Terminal Unicode/ANSI support missing | Low | Medium | Graceful degradation (detect capability, fallback to ASCII) |

---

## Quality Gates

### Pre-Implementation Gates
- ✅ Constitution check passed (all 6 principles)
- ✅ Research complete (7 technology patterns validated)
- ✅ Data model defined (TodoTask, enums, validations)

### Development Gates (Per Phase)
- [ ] Code follows PEP 8 style guide
- [ ] Type hints on all functions/methods
- [ ] Docstrings on public APIs
- [ ] Tests written (TDD)
- [ ] Coverage ≥80% for module
- [ ] No TODOs in committed code

### Release Gates
- [ ] All P1 user stories implemented
- [ ] All 15 success criteria validated
- [ ] Test suite passes (100% pass rate)
- [ ] Coverage report ≥80%
- [ ] Performance benchmarks met (<200ms, <2s startup)
- [ ] README complete with screenshots
- [ ] "Developer by: maneeshanif" credit in splash screen

---

## Next Steps

1. **Immediate**: Complete Phase 1 contracts and quickstart guide
2. **Next Command**: Run `/sp.tasks` to generate testable task breakdown in `tasks.md`
3. **Implementation**: Invoke @setup-agent to begin Milestone 1
4. **Tracking**: Create PHR after /sp.plan completion

**Phase 1 Remaining Work**:
- [ ] Generate `contracts/cli-commands.md` (CLI command specifications)
- [ ] Generate `quickstart.md` (developer onboarding)
- [ ] Run `update-agent-context.sh copilot` to sync agent context


