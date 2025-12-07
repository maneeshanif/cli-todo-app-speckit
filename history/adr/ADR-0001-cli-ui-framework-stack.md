# ADR-0001: CLI UI Framework Stack

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** 001-retro-todo-app
- **Context:** The retro todo CLI requires a cohesive UI framework that delivers cyberpunk aesthetics while maintaining excellent developer ergonomics and terminal compatibility.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - All UI code depends on this stack
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Click, argparse, curses evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects splash, tables, prompts, animations, TUI -->

## Decision

Adopt a unified CLI UI stack composed of four complementary libraries:

| Component | Library | Version | Responsibility |
|-----------|---------|---------|----------------|
| CLI Framework | Typer | 0.9+ | Command routing, argument parsing, help generation |
| Terminal Formatting | Rich | 13.0+ | Colors, tables, panels, progress bars, markup |
| Interactive Prompts | Questionary | 2.0+ | Select menus, confirmations, text input with styling |
| ASCII Art | PyFiglet | 0.8+ | Splash screen banner and decorative text |
| Multi-page TUI | Textual | 0.40+ | Optional advanced interface (Phase II) |

**Integration Strategy:**
- Use `typer.Typer(rich_markup_mode="rich")` for unified styling in help text
- Share single `Console()` instance across all modules for consistent output
- Apply custom `retro_style` to all Questionary prompts for cohesive aesthetics
- Use "slant" font in PyFiglet for optimal width/readability balance

**Color Palette (Constitutional):**
- Cyan (#00FFFF): Primary accent, question marks, pointers
- Magenta (#FF00FF): Highlights, question text, borders
- Green (#00FF00): Success states, answers, completed items
- Yellow (#FFFF00): Warnings, separators, caution indicators

## Consequences

### Positive

- **Unified aesthetics**: All UI components share the cyberpunk visual language
- **Excellent DX**: Typer provides automatic help generation and type inference
- **Battle-tested**: Rich has 40k+ GitHub stars, extensive documentation
- **Flexible integration**: Components work independently or together
- **Keyboard-first**: All interactions support keyboard-only navigation
- **Cross-platform**: Works on Linux, macOS, Windows with ANSI support

### Negative

- **Bundle size**: Four libraries increases dependency footprint (~5MB)
- **Learning curve**: Team must understand Rich markup syntax and Questionary patterns
- **Styling coordination**: Custom theme requires maintenance across all prompt types
- **Textual complexity**: Optional TUI adds significant complexity if activated

## Alternatives Considered

### Alternative A: Click + curses + basic ANSI

- **Pros**: Minimal dependencies, full terminal control
- **Cons**: No Rich tables/panels, manual ANSI escape codes, poor Windows support
- **Why rejected**: Significantly higher implementation effort for inferior visual results

### Alternative B: argparse + colorama + tabulate

- **Pros**: Standard library CLI parsing, simple colored output
- **Cons**: No automatic help styling, no interactive prompts, no ASCII art
- **Why rejected**: Lacks visual flair required by Retro-First UI principle (NON-NEGOTIABLE)

### Alternative C: Prompt Toolkit + Click

- **Pros**: Powerful prompt toolkit for complex interactions
- **Cons**: Steeper learning curve, less intuitive than Questionary for simple flows
- **Why rejected**: Over-engineered for target use case, Questionary provides sufficient capability

## References

- Feature Spec: [specs/001-retro-todo-app/spec.md](../../specs/001-retro-todo-app/spec.md)
- Implementation Plan: [specs/001-retro-todo-app/plan.md](../../specs/001-retro-todo-app/plan.md)
- Research Evidence: [specs/001-retro-todo-app/research.md](../../specs/001-retro-todo-app/research.md) (Sections 1, 2, 7)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Principles I, VI)
