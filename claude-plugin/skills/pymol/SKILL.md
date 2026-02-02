---
name: pymol
description: Use when user runs /pymol command to launch PyMOL and establish a controllable session
---

# Launch PyMOL Session

Launch PyMOL with Claude socket plugin and establish connection.

## Execution

```python
from claudemol import launch_pymol, PyMOLConnection

# Launch PyMOL (waits for socket to be ready)
process = launch_pymol()

# Connect
conn = PyMOLConnection()
conn.connect()
print("PyMOL is running and connected")
```

## After Launch

Report to user:
- PyMOL is running and connected
- Ready to receive commands

Offer next steps:
- "Load a structure" (fetch from PDB or load local file)
- "Show me what's loaded" (list current objects)

## Sending Commands

```python
# Fetch a structure
conn.execute("cmd.fetch('1ubq')")

# Multiple commands
conn.execute("""
cmd.hide('everything')
cmd.show('cartoon')
cmd.color('spectrum')
cmd.orient()
""")

# Get object names
result = conn.execute("print(cmd.get_names())")
```

## If Connection Fails

Check if PyMOL setup is complete. Suggest running `/pymol-setup` if:
- PyMOL not found in PATH
- Socket plugin not configured
- Connection timeout

## Related Skills

- @pymol-fundamentals - PyMOL command reference
- @pymol-setup - First-time configuration
