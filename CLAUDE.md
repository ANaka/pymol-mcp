# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ai-mol integrates PyMOL (molecular visualization software) with Claude Code. It enables Claude to control PyMOL via natural language commands for structural biology and molecular visualization tasks.

## Architecture

```
Claude Code → TCP Socket (port 9880) → PyMOL Plugin → cmd.* execution
```

**Key components:**

1. **PyMOL Plugin** (`claude_socket_plugin.py`) - Headless socket listener that runs inside PyMOL
   - Auto-loads via `~/.pymolrc`
   - Accepts TCP connections on localhost:9880
   - Executes received Python code via `exec()` with output capture
   - Commands: `claude_status`, `claude_stop`, `claude_start`

2. **Connection Module** (`pymol_connection.py`) - Python module for socket communication
   - `PyMOLConnection` class handles TCP socket communication
   - Used by Claude Code to send commands to PyMOL

## Known Issues

**View Inflation Bug (FIXED):** When using `cmd.png(path, width, height)` with explicit dimensions, PyMOL's view matrix can become corrupted after multiple reinitialize cycles. Always use `cmd.ray(width, height)` followed by `cmd.png(path)` without dimensions to prevent this.

## Claude Code Workflow

**First-time setup:** Run `/pymol-setup` or ask Claude to set up PyMOL.

**Starting a session:** Say "open PyMOL" or "load <structure>". Claude will launch PyMOL if needed.

**PyMOL commands (run in PyMOL console):**
- `claude_status` - Check if listener is running
- `claude_stop` - Stop listener
- `claude_start` - Start listener

## Development Commands

```bash
# Linting (ruff configured for E, F, I rules)
ruff check .
ruff format .

# Type checking
pyright
```

## Development Goals

A main goal of this project is to build out a good set of skills for Claude to interact with PyMOL. When you learn something important about PyMOL commands, common workflows, or useful patterns, consider adding it as a skill.

## Key Code Patterns

- Global connection singleton via `get_pymol_connection()` with auto-reconnect
- Plugin handles multiple clients but only one active connection at a time
- Skills in `.claude/skills/` provide workflow guidance for common tasks
