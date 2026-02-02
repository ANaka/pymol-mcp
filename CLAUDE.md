# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ai-mol integrates PyMOL (molecular visualization software) with Claude Code. It enables Claude to control PyMOL via natural language commands for structural biology and molecular visualization tasks.

## Repository Structure

```
ai-mol/
├── src/ai_mol/           # pip package
│   ├── connection.py     # PyMOLConnection class
│   ├── session.py        # Session management
│   ├── view.py           # Visual feedback helpers
│   ├── plugin.py         # Socket plugin (runs in PyMOL)
│   └── cli.py            # CLI: ai-mol setup|status|test
├── claude-plugin/        # Claude Code plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/           # All visualization skills
└── .claude/skills/       # Local skills (for development)
```

## Architecture

```
Claude Code → TCP Socket (port 9880) → PyMOL Plugin → cmd.* execution
```

**Key components:**

1. **PyMOL Plugin** (`src/ai_mol/plugin.py`) - Socket listener that runs inside PyMOL
   - Auto-loads via `~/.pymolrc` after `ai-mol setup`
   - Accepts TCP connections on localhost:9880
   - Executes received Python code via `exec()` with output capture
   - Commands: `claude_status`, `claude_stop`, `claude_start`

2. **Connection Module** (`src/ai_mol/connection.py`) - Python module for socket communication
   - `PyMOLConnection` class handles TCP socket communication
   - Used by Claude Code to send commands to PyMOL

3. **Skills** (`claude-plugin/skills/`) - Workflow guidance for visualization tasks
   - Distributed as Claude Code plugin separately from pip package

## Distribution

**pip package:**
```bash
pip install ai-mol
ai-mol setup  # Configures PyMOL to auto-load plugin
```

**Claude Code skills:**
```bash
/plugin marketplace add ANaka/ai-mol?path=claude-plugin
/plugin install ai-mol-skills
```

## Known Issues

**View Inflation Bug (FIXED):** When using `cmd.png(path, width, height)` with explicit dimensions, PyMOL's view matrix can become corrupted after multiple reinitialize cycles. Always use `cmd.ray(width, height)` followed by `cmd.png(path)` without dimensions to prevent this.

## Development Commands

```bash
# Install locally for development
pip install -e .

# Linting (ruff configured for E, F, I rules)
ruff check src/
ruff format src/

# Type checking
pyright

# Run tests
pytest tests/
```

## Key Code Patterns

- `from ai_mol import PyMOLConnection, PyMOLSession` - Main API
- Global session via `get_session()` with auto-reconnect
- Plugin handles multiple clients but only one active connection at a time
- Local skills in `.claude/skills/` for development, `claude-plugin/skills/` for distribution
