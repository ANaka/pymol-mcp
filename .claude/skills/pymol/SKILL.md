---
name: pymol
description: Use when user runs /pymol command to launch PyMOL and establish a controllable session
---

# Launch PyMOL Session

Launch PyMOL with Claude socket plugin and establish connection.

## Execution

Run from the ai-mol repo root:

```bash
python launch_pymol.py
```

## After Launch

Report to user:
- PyMOL is running and connected
- Ready to receive commands

Offer next steps:
- "Load a structure" (fetch from PDB or load local file)
- "Show me what's loaded" (list current objects)

## Sending Commands

Use `pymol_cmd.py` to send commands:

```bash
# Fetch a structure
python pymol_cmd.py "fetch 1ubq"

# Multiple commands
python pymol_cmd.py "hide everything; show cartoon; color spectrum; orient"

# Get object names
python pymol_cmd.py "print(cmd.get_names())"
```

## If Connection Fails

Check if PyMOL setup is complete. Suggest running `/pymol-setup` if:
- PyMOL not found in PATH
- Socket plugin not configured
- Connection timeout

## Related Skills

- @pymol-fundamentals - PyMOL command reference
- @pymol-setup - First-time configuration
