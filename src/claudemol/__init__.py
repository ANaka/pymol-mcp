"""
claudemol: PyMOL integration for Claude Code

Connect to PyMOL via socket for AI-assisted molecular visualization.
"""

from claudemol.connection import (
    PyMOLConnection,
    connect_or_launch,
    launch_pymol,
    find_pymol_command,
    check_pymol_installed,
)
from claudemol.session import (
    PyMOLSession,
    get_session,
    ensure_running,
    stop_pymol,
)

__version__ = "0.1.0"
__all__ = [
    "PyMOLConnection",
    "PyMOLSession",
    "connect_or_launch",
    "launch_pymol",
    "find_pymol_command",
    "check_pymol_installed",
    "get_session",
    "ensure_running",
    "stop_pymol",
]
