# Implementation Tasks: Retro Terminal Todo Manager

**Feature**: 001-retro-todo-app  
**Branch**: `001-retro-todo-app`  
**Created**: 2025-12-07  
**Status**: Ready for Implementation

## Overview

This document breaks down the implementation into testable, atomic tasks organized by user story. Following TDD (Test-Driven Development) principles from the constitution, tests are written before implementation (Red-Green-Refactor).

**Total Tasks**: 83  
**Parallelizable Tasks**: 42  
**User Stories**: 7 (P1: 1 story, P2: 3 stories, P3: 3 stories)

**Suggested MVP**: Complete Phase 1-3 (User Story 1 only) for functional todo app

---

## Task Organization

Tasks are organized in phases:
1. **Setup** - Project initialization
2. **Foundational** - Core infrastructure needed by all stories
3. **User Story 1 (P1)** - Basic Task Management (MVP)
4. **User Story 2 (P2)** - Task Organization
5. **User Story 3 (P2)** - Task Discovery (Search/Filter)
6. **User Story 5 (P2)** - Task Updates and Deletion
7. **User Story 4 (P3)** - Task Sorting
8. **User Story 6 (P3)** - Due Dates and Reminders
9. **User Story 7 (P3)** - Recurring Tasks
10. **Polish** - Cross-cutting concerns

---

## Phase 1: Setup (Project Initialization)

**Goal**: Bootstrap project with uv, configure dependencies, establish directory structure.

**Tasks**:

- [ ] T001 Run `uv init` to create pyproject.toml in project root
- [ ] T002 [P] Add production dependencies: `uv add typer[all] rich textual pydantic tinydb questionary pyfiglet python-dateutil`
- [ ] T003 [P] Add dev dependencies: `uv add --dev pytest pytest-cov`
- [ ] T004 Create directory structure: `retro_todo/{models,database,services,ui}` with `__init__.py` files
- [ ] T005 Create directory structure: `tests/{unit,integration,e2e}` with `__init__.py` and `conftest.py`
- [ ] T006 Create `retro_todo/__init__.py` with `__version__ = "0.1.0"`
- [ ] T007 [P] Create `.gitignore` with entries: `todo_data.json`, `__pycache__`, `.pytest_cache`, `.coverage`, `htmlcov/`, `.venv/`
- [ ] T008 [P] Configure pytest in `pyproject.toml` with coverage settings (minimum 80%)
- [ ] T009 Verify setup: `uv run pytest` executes successfully (no tests yet)

**Verification**: `uv.lock` exists, all dependencies installed, directory structure matches plan.md

---

## Phase 2: Foundational (Core Infrastructure)

**Goal**: Implement data models, database layer, and UI theme that all user stories depend on.

### Models Layer

- [ ] T010 [RED] Write test for Priority enum in `tests/unit/test_enums.py` (color property, icon property)
- [ ] T011 [GREEN] Implement Priority enum in `retro_todo/models/enums.py` with LOW/MEDIUM/HIGH/URGENT values
- [ ] T012 [RED] Write test for Status enum in `tests/unit/test_enums.py` (icon property, display_style)
- [ ] T013 [GREEN] Implement Status enum in `retro_todo/models/enums.py` with PENDING/COMPLETED values
- [ ] T014 [RED] Write test for RecurrencePattern enum in `tests/unit/test_enums.py`
- [ ] T015 [GREEN] Implement RecurrencePattern enum in `retro_todo/models/enums.py` with NONE/DAILY/WEEKLY/MONTHLY
- [ ] T016 [RED] Write test for TodoTask model validation in `tests/unit/test_models.py` (title non-empty, due_date future)
- [ ] T017 [GREEN] Implement TodoTask Pydantic model in `retro_todo/models/todo.py` with all 11 fields
- [ ] T018 [RED] Write test for TodoTask.mark_complete() method in `tests/unit/test_models.py`
- [ ] T019 [GREEN] Implement TodoTask business logic methods (mark_complete, is_overdue, has_recurrence)
- [ ] T020 [RED] Write test for TodoTask serialization (to_dict/from_dict) in `tests/unit/test_models.py`
- [ ] T021 [GREEN] Implement TodoTask.to_dict() and TodoTask.from_dict() for TinyDB compatibility

### Database Layer

- [ ] T022 [RED] Write test for database initialization in `tests/integration/test_database.py`
- [ ] T023 [GREEN] Implement TinyDB wrapper in `retro_todo/database/db.py` with CachingMiddleware
- [ ] T024 [RED] Write test for ID generation atomicity in `tests/unit/test_id_generator.py`
- [ ] T025 [GREEN] Implement atomic ID generator in `retro_todo/database/id_generator.py`
- [ ] T026 [RED] Write test for database CRUD operations in `tests/integration/test_database.py`
- [ ] T027 [GREEN] Implement database helper methods (insert, get, update, delete, all) in `retro_todo/database/db.py`

### UI Theme

- [ ] T028 [P] Create cyberpunk color constants in `retro_todo/ui/theme.py` (CYAN, MAGENTA, GREEN, YELLOW, RED)
- [ ] T029 [P] Create retro questionary style in `retro_todo/ui/theme.py` with cyberpunk colors

**Verification**: All foundational tests pass, models serialize correctly, database persists data, theme constants available.

---

## Phase 3: User Story 1 - Basic Task Management (P1) 🎯 MVP

**Story Goal**: User can launch app, see splash screen, add tasks, view list, mark complete, persist data.

**Independent Test**: Launch → Splash → Add task with title/priority → View list → Mark complete → Restart → Data persists

### UI Components

- [ ] T030 [RED] [US1] Write test for splash screen rendering in `tests/unit/test_splash.py`
- [ ] T031 [GREEN] [US1] Implement splash screen with PyFiglet in `retro_todo/ui/splash.py` (include "Developer by: maneeshanif")
- [ ] T032 [RED] [US1] Write test for task table rendering in `tests/unit/test_tables.py`
- [ ] T033 [GREEN] [US1] Implement Rich table renderer in `retro_todo/ui/tables.py` (format_task_table with colors)
- [ ] T034 [RED] [US1] Write test for add task prompt in `tests/unit/test_prompts.py`
- [ ] T035 [GREEN] [US1] Implement add task prompt form in `retro_todo/ui/prompts.py` (title, priority using questionary)

### Services Layer

- [ ] T036 [RED] [US1] Write test for TodoService.create() in `tests/integration/test_todo_service.py`
- [ ] T037 [GREEN] [US1] Implement TodoService.create() in `retro_todo/services/todo_service.py`
- [ ] T038 [RED] [US1] Write test for TodoService.get_all() in `tests/integration/test_todo_service.py`
- [ ] T039 [GREEN] [US1] Implement TodoService.get_all() in `retro_todo/services/todo_service.py`
- [ ] T040 [RED] [US1] Write test for TodoService.complete() in `tests/integration/test_todo_service.py`
- [ ] T041 [GREEN] [US1] Implement TodoService.complete() in `retro_todo/services/todo_service.py`

### CLI Commands

- [ ] T042 [RED] [US1] Write test for `retro-todo` splash command in `tests/e2e/test_cli_commands.py`
- [ ] T043 [GREEN] [US1] Implement Typer app initialization in `retro_todo/main.py` with rich_markup_mode
- [ ] T044 [GREEN] [US1] Implement splash command in `retro_todo/main.py`
- [ ] T045 [RED] [US1] Write test for `retro-todo add` command in `tests/e2e/test_cli_commands.py`
- [ ] T046 [GREEN] [US1] Implement add command in `retro_todo/main.py` (calls prompt → service.create)
- [ ] T047 [RED] [US1] Write test for `retro-todo list` command in `tests/e2e/test_cli_commands.py`
- [ ] T048 [GREEN] [US1] Implement list command in `retro_todo/main.py` (calls service.get_all → table renderer)
- [ ] T049 [RED] [US1] Write test for `retro-todo complete` command in `tests/e2e/test_cli_commands.py`
- [ ] T050 [GREEN] [US1] Implement complete command in `retro_todo/main.py` (calls service.complete)

### Integration

- [ ] T051 [US1] Run full test suite for User Story 1: `uv run pytest tests/ -k "us1 or US1" --cov=retro_todo`
- [ ] T052 [US1] Verify coverage ≥80% for User Story 1 modules
- [ ] T053 [US1] Manual acceptance test: Launch → Add → List → Complete → Restart → Verify persistence

**US1 Deliverable**: Functional MVP with splash, add, list, complete commands. Data persists via TinyDB.

---

## Phase 4: User Story 2 - Task Organization (P2)

**Story Goal**: User can add descriptions, tags, view statistics, see priority color indicators.

**Independent Test**: Add task with description + tags → View list with color coding → View stats panel

### UI Enhancements

- [ ] T054 [RED] [US2] Write test for description prompt in `tests/unit/test_prompts.py`
- [ ] T055 [GREEN] [US2] Add description field to add_task_prompt in `retro_todo/ui/prompts.py`
- [ ] T056 [RED] [US2] Write test for tags prompt in `tests/unit/test_prompts.py`
- [ ] T057 [GREEN] [US2] Add tags field to add_task_prompt in `retro_todo/ui/prompts.py` (comma-separated input)
- [ ] T058 [RED] [US2] Write test for stats panel rendering in `tests/unit/test_tables.py`
- [ ] T059 [GREEN] [US2] Implement stats panel renderer in `retro_todo/ui/tables.py` (priority counts, tag counts)

### Services Layer

- [ ] T060 [RED] [US2] Write test for TodoService.get_statistics() in `tests/integration/test_todo_service.py`
- [ ] T061 [GREEN] [US2] Implement TodoService.get_statistics() in `retro_todo/services/todo_service.py`

### CLI Commands

- [ ] T062 [RED] [US2] Write test for `retro-todo stats` command in `tests/e2e/test_cli_commands.py`
- [ ] T063 [GREEN] [US2] Implement stats command in `retro_todo/main.py` (calls service.get_statistics)

### Integration

- [ ] T064 [US2] Run test suite for User Story 2: `uv run pytest tests/ -k "us2 or US2" --cov=retro_todo`
- [ ] T065 [US2] Manual acceptance test: Add task with tags → View stats → Verify color coding

**US2 Deliverable**: Tasks support descriptions and tags, stats panel shows breakdowns.

---

## Phase 5: User Story 3 - Task Discovery (P2)

**Story Goal**: User can search by keyword, filter by priority/status/tags, combine filters.

**Independent Test**: Search "login" → Filter by priority + status → Combine filters → Verify highlighted results

### Services Layer

- [ ] T066 [RED] [US3] Write test for SearchService.search() in `tests/integration/test_search.py`
- [ ] T067 [GREEN] [US3] Implement SearchService.search() in `retro_todo/services/search_service.py` (fuzzy search in title/description)
- [ ] T068 [RED] [US3] Write test for SearchService.filter() in `tests/integration/test_search.py`
- [ ] T069 [GREEN] [US3] Implement SearchService.filter() in `retro_todo/services/search_service.py` (multi-criteria AND logic)

### UI Components

- [ ] T070 [RED] [US3] Write test for search result highlighting in `tests/unit/test_tables.py`
- [ ] T071 [GREEN] [US3] Add highlight_search_term() to `retro_todo/ui/tables.py`
- [ ] T072 [RED] [US3] Write test for filter selection prompt in `tests/unit/test_prompts.py`
- [ ] T073 [GREEN] [US3] Implement filter_prompt() in `retro_todo/ui/prompts.py` (multi-select checkboxes)

### CLI Commands

- [ ] T074 [RED] [US3] Write test for `retro-todo search` command in `tests/e2e/test_cli_commands.py`
- [ ] T075 [GREEN] [US3] Implement search command in `retro_todo/main.py`
- [ ] T076 [RED] [US3] Write test for `retro-todo filter` command in `tests/e2e/test_cli_commands.py`
- [ ] T077 [GREEN] [US3] Implement filter command in `retro_todo/main.py`

### Integration

- [ ] T078 [US3] Run test suite for User Story 3: `uv run pytest tests/ -k "us3 or US3" --cov=retro_todo`
- [ ] T079 [US3] Manual acceptance test: Search → Filter → Combine → Verify results

**US3 Deliverable**: Search and filter functionality with highlighted results.

---

## Phase 6: User Story 5 - Task Updates and Deletion (P2)

**Story Goal**: User can update any task field, see diff, delete with confirmation.

**Independent Test**: Update task priority → See diff → Delete task → Confirm → Verify removed

### UI Components

- [ ] T080 [RED] [US5] Write test for update prompt in `tests/unit/test_prompts.py`
- [ ] T081 [GREEN] [US5] Implement update_task_prompt() in `retro_todo/ui/prompts.py` (field selection menu)
- [ ] T082 [RED] [US5] Write test for delete confirmation in `tests/unit/test_prompts.py`
- [ ] T083 [GREEN] [US5] Implement delete_confirmation_prompt() in `retro_todo/ui/prompts.py`
- [ ] T084 [RED] [US5] Write test for diff display in `tests/unit/test_tables.py`
- [ ] T085 [GREEN] [US5] Implement format_diff() in `retro_todo/ui/tables.py` (before/after comparison)

### Services Layer

- [ ] T086 [RED] [US5] Write test for TodoService.update() in `tests/integration/test_todo_service.py`
- [ ] T087 [GREEN] [US5] Implement TodoService.update() in `retro_todo/services/todo_service.py`
- [ ] T088 [RED] [US5] Write test for TodoService.delete() in `tests/integration/test_todo_service.py`
- [ ] T089 [GREEN] [US5] Implement TodoService.delete() in `retro_todo/services/todo_service.py`

### CLI Commands

- [ ] T090 [RED] [US5] Write test for `retro-todo update` command in `tests/e2e/test_cli_commands.py`
- [ ] T091 [GREEN] [US5] Implement update command in `retro_todo/main.py`
- [ ] T092 [RED] [US5] Write test for `retro-todo delete` command in `tests/e2e/test_cli_commands.py`
- [ ] T093 [GREEN] [US5] Implement delete command in `retro_todo/main.py`

### Integration

- [ ] T094 [US5] Run test suite for User Story 5: `uv run pytest tests/ -k "us5 or US5" --cov=retro_todo`
- [ ] T095 [US5] Manual acceptance test: Update → See diff → Delete → Confirm

**US5 Deliverable**: Update and delete commands with diff view and confirmation.

---

## Phase 7: User Story 4 - Task Sorting (P3)

**Story Goal**: User can sort by priority/date/title, toggle direction, persist preference.

**Independent Test**: Sort by priority → Toggle direction → Sort by date → Restart → Preference persists

### Services Layer

- [ ] T096 [RED] [US4] Write test for SortService.sort() in `tests/integration/test_sort.py`
- [ ] T097 [GREEN] [US4] Implement SortService.sort() in `retro_todo/services/sort_service.py` (multiple keys)
- [ ] T098 [RED] [US4] Write test for sort preference persistence in `tests/integration/test_sort.py`
- [ ] T099 [GREEN] [US4] Add sort preference to TinyDB config in `retro_todo/database/db.py`

### CLI Commands

- [ ] T100 [RED] [US4] Write test for `retro-todo sort` command in `tests/e2e/test_cli_commands.py`
- [ ] T101 [GREEN] [US4] Implement sort command in `retro_todo/main.py` (with --reverse flag)

### Integration

- [ ] T102 [US4] Run test suite for User Story 4: `uv run pytest tests/ -k "us4 or US4" --cov=retro_todo`
- [ ] T103 [US4] Manual acceptance test: Sort → Toggle → Restart → Verify persistence

**US4 Deliverable**: Sort functionality with multiple keys and persisted preferences.

---

## Phase 8: User Story 6 - Due Dates and Reminders (P3)

**Story Goal**: User can add due dates with natural language, see countdowns, filter by date ranges.

**Independent Test**: Add task "tomorrow" → See countdown → Filter "Due Today" → Overdue icon appears

### Services Layer

- [ ] T104 [RED] [US6] Write test for date parsing in `tests/unit/test_date_parser.py`
- [ ] T105 [GREEN] [US6] Implement parse_natural_date() in `retro_todo/services/date_parser.py` (dateutil wrapper)
- [ ] T106 [RED] [US6] Write test for overdue detection in `tests/integration/test_todo_service.py`
- [ ] T107 [GREEN] [US6] Implement TodoService.get_overdue() in `retro_todo/services/todo_service.py`
- [ ] T108 [RED] [US6] Write test for date range filter in `tests/integration/test_search.py`
- [ ] T109 [GREEN] [US6] Add date range filter to SearchService.filter() in `retro_todo/services/search_service.py`

### UI Components

- [ ] T110 [RED] [US6] Write test for due date prompt in `tests/unit/test_prompts.py`
- [ ] T111 [GREEN] [US6] Add due_date field to prompts in `retro_todo/ui/prompts.py` (natural language input)
- [ ] T112 [RED] [US6] Write test for countdown display in `tests/unit/test_tables.py`
- [ ] T113 [GREEN] [US6] Implement format_due_date_display() in TodoTask model (countdown logic)

### CLI Commands

- [ ] T114 [RED] [US6] Write test for date filter options in `tests/e2e/test_cli_commands.py`
- [ ] T115 [GREEN] [US6] Add --due-today and --due-week flags to list command in `retro_todo/main.py`

### Integration

- [ ] T116 [US6] Run test suite for User Story 6: `uv run pytest tests/ -k "us6 or US6" --cov=retro_todo`
- [ ] T117 [US6] Manual acceptance test: Add "tomorrow" → See countdown → Filter → Overdue icon

**US6 Deliverable**: Due dates with natural language parsing and visual warnings.

---

## Phase 9: User Story 7 - Recurring Tasks (P3)

**Story Goal**: User can create recurring tasks, complete them, auto-generate next occurrence.

**Independent Test**: Create daily task → Complete → Verify next occurrence generated with same details

### Services Layer

- [ ] T118 [RED] [US7] Write test for RecurrenceService.generate_next() in `tests/integration/test_recurrence.py`
- [ ] T119 [GREEN] [US7] Implement RecurrenceService.generate_next() in `retro_todo/services/recurrence_service.py`
- [ ] T120 [RED] [US7] Write test for completion with recurrence in `tests/integration/test_todo_service.py`
- [ ] T121 [GREEN] [US7] Modify TodoService.complete() to call RecurrenceService when pattern != NONE

### UI Components

- [ ] T122 [RED] [US7] Write test for recurrence prompt in `tests/unit/test_prompts.py`
- [ ] T123 [GREEN] [US7] Add recurrence_pattern field to prompts in `retro_todo/ui/prompts.py`
- [ ] T124 [RED] [US7] Write test for recurrence badge display in `tests/unit/test_tables.py`
- [ ] T125 [GREEN] [US7] Add recurrence badge to table renderer in `retro_todo/ui/tables.py`

### Integration

- [ ] T126 [US7] Run test suite for User Story 7: `uv run pytest tests/ -k "us7 or US7" --cov=retro_todo`
- [ ] T127 [US7] Manual acceptance test: Create daily → Complete → Verify next occurrence

**US7 Deliverable**: Recurring tasks with automatic next occurrence generation.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Goal**: Animations, error handling, documentation, final testing.

### Animations & UX Polish

- [ ] T128 [P] Implement completion celebration animation in `retro_todo/ui/animations.py` (Rich spinner + confetti)
- [ ] T129 [P] Add loading spinners for operations >100ms in `retro_todo/ui/animations.py`
- [ ] T130 [P] Implement empty state messages across all commands in `retro_todo/main.py`

### Error Handling

- [ ] T131 [P] Add global error handler in `retro_todo/main.py` (catch exceptions, show friendly messages)
- [ ] T132 [P] Add database corruption recovery in `retro_todo/database/db.py`
- [ ] T133 [P] Add validation error messages in all prompts in `retro_todo/ui/prompts.py`

### Documentation

- [ ] T134 [P] Create README.md with installation instructions, usage examples, screenshots
- [ ] T135 [P] Add docstrings to all public APIs (models, services, CLI commands)
- [ ] T136 [P] Create CHANGELOG.md for v0.1.0

### Final Testing

- [ ] T137 Run full test suite: `uv run pytest tests/ --cov=retro_todo --cov-report=term-missing`
- [ ] T138 Verify coverage ≥80% across all modules
- [ ] T139 Run end-to-end workflow test covering all 7 user stories
- [ ] T140 Performance test: Verify <200ms operations with 1000 tasks
- [ ] T141 Performance test: Verify <2s startup time

### Release Preparation

- [ ] T142 Update version to 1.0.0 in `retro_todo/__init__.py`
- [ ] T143 Generate uv.lock with final dependency versions
- [ ] T144 Tag release: `git tag v1.0.0`

**Polish Deliverable**: Production-ready app with animations, error handling, documentation.

---

## Dependency Graph (User Story Completion Order)

```
Setup (Phase 1)
    ↓
Foundational (Phase 2)
    ↓
┌───────────────────────────────────────┐
│ User Story 1 (P1) - REQUIRED FOR MVP │
└───────────────┬───────────────────────┘
                ↓
    ┌───────────┴───────────┐
    ↓                       ↓
User Story 2 (P2)    User Story 3 (P2)
Task Organization    Task Discovery
    ↓                       ↓
User Story 5 (P2)           │
Task Updates/Delete         │
    ↓                       ↓
User Story 4 (P3) ← ← ← ← ← ┘
Task Sorting
    ↓
User Story 6 (P3)
Due Dates/Reminders
    ↓
User Story 7 (P3)
Recurring Tasks
    ↓
Polish (Phase 10)
```

**Critical Path**: Setup → Foundational → US1 → US2 → US5 → US4 → US6 → US7 → Polish

**Independent Stories** (Can be developed in parallel after US1):
- US2 (Task Organization)
- US3 (Task Discovery)

---

## Parallel Execution Opportunities

### Phase 1 (Setup)
**Parallel**: T002, T003, T005, T007, T008 (different files, no dependencies)

### Phase 2 (Foundational)
**Parallel Groups**:
- Group A: T010-T021 (Models layer)
- Group B: T022-T027 (Database layer) - AFTER models complete
- Group C: T028-T029 (UI theme) - Independent

### Phase 3 (User Story 1)
**Parallel Groups**:
- Group A: T030-T035 (UI components)
- Group B: T036-T041 (Services) - AFTER models/database
- Group C: T042-T050 (CLI commands) - AFTER UI + services

### Phase 4-9 (User Stories 2-7)
Each user story can be developed by separate developers simultaneously after US1 completes.

### Phase 10 (Polish)
**Parallel**: T128-T136 (all polish tasks independent)

---

## Implementation Strategy

### Recommended Approach

1. **Week 1 Focus**: Complete Setup + Foundational + US1 (MVP)
   - Deliverable: Functional todo app with add/list/complete
   - Milestone: Demo-able product

2. **Week 2 Focus**: Add US2 + US3 + US5 (Core features)
   - Deliverable: Full-featured task manager
   - Milestone: Feature-complete for basic use

3. **Week 3 Focus**: Add US4 + US6 + US7 (Advanced features)
   - Deliverable: Power user features
   - Milestone: All user stories implemented

4. **Week 4 Focus**: Polish + Testing + Documentation
   - Deliverable: Production-ready release
   - Milestone: v1.0.0 launch

### TDD Workflow Per Task

For each [RED]/[GREEN] task pair:

1. **RED**: Write failing test
   ```bash
   uv run pytest tests/unit/test_file.py::test_name
   # Expected: FAILED (test should fail)
   ```

2. **GREEN**: Implement minimum code to pass
   ```bash
   uv run pytest tests/unit/test_file.py::test_name
   # Expected: PASSED
   ```

3. **REFACTOR**: Clean up code, add type hints, docstrings
   ```bash
   uv run pytest tests/unit/test_file.py::test_name
   # Expected: PASSED (still passing after refactor)
   ```

### Coverage Verification

After each user story phase:
```bash
uv run pytest tests/ -k "US#" --cov=retro_todo --cov-report=term-missing
# Verify ≥80% coverage for that story's modules
```

---

## Success Criteria

### MVP Success (After Phase 3 - User Story 1)
- ✅ User can add tasks with title and priority
- ✅ User can view task list with color coding
- ✅ User can mark tasks complete
- ✅ Data persists between sessions
- ✅ Splash screen displays with developer credit
- ✅ Test coverage ≥80% for implemented modules

### Full Release Success (After Phase 9)
- ✅ All 7 user stories implemented
- ✅ All 37 functional requirements met
- ✅ All 15 success criteria validated
- ✅ Test coverage ≥80% across all modules
- ✅ Performance targets met (<200ms, <2s startup)
- ✅ Constitution principles verified (6/6 passed)

---

## Notes

**Parallelization**: 42 tasks marked [P] can be executed concurrently by multiple developers or AI agents.

**TDD Enforcement**: Constitution principle III mandates Red-Green-Refactor. All implementation tasks have corresponding test tasks.

**Story Independence**: Each user story (except US1 which is foundational) can be developed and tested independently, enabling parallel development.

**MVP Priority**: User Story 1 alone provides a functional todo app. Recommend deploying MVP after Phase 3 for early feedback.

**Task IDs**: Sequential T001-T144 for easy tracking. Use `[US#]` labels to filter tasks by story.

**File Paths**: Every task specifies exact file path for LLM execution clarity.

---

**Next Step**: Begin implementation with Phase 1 (Setup) tasks T001-T009.

**Developer by: maneeshanif**
