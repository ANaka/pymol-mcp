"""
Visual feedback helper for PyMOL.

Provides a simple way to execute commands and save/view the result.

Usage:
    from ai_mol.view import pymol_view

    # Execute commands and save a snapshot
    path = pymol_view("cmd.fetch('1ubq'); cmd.show('cartoon')", name="ubq_cartoon")

    # Or with auto-naming
    path = pymol_view("cmd.color('red', 'all')")
"""

import json
import socket
import time
from datetime import datetime
from pathlib import Path

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9880
SCRATCH_DIR = Path.home() / ".ai-mol" / "scratch"


def ensure_scratch_dir():
    """Ensure the scratch directory exists."""
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    return SCRATCH_DIR


def send_command(code: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, timeout: float = 120.0) -> dict:
    """Send a command to PyMOL and return the result."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        msg = json.dumps({"type": "execute", "code": code})
        s.sendall(msg.encode())

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
            try:
                return json.loads(response.decode())
            except json.JSONDecodeError:
                continue
    finally:
        s.close()
    return {"status": "error", "error": "No response received"}


def generate_filename(name: str | None = None, extension: str = "png") -> Path:
    """Generate a unique filename in the scratch directory."""
    ensure_scratch_dir()

    if name:
        # Clean the name
        clean_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        return SCRATCH_DIR / f"{clean_name}.{extension}"
    else:
        # Auto-generate with timestamp
        timestamp = datetime.now().strftime("%H%M%S")
        return SCRATCH_DIR / f"view_{timestamp}.{extension}"


def pymol_view(
    commands: str,
    name: str | None = None,
    width: int = 800,
    height: int = 600,
    ray: bool = False,
    port: int = DEFAULT_PORT,
) -> str:
    """
    Execute PyMOL commands and save a snapshot.

    Args:
        commands: PyMOL Python commands to execute (e.g., "cmd.fetch('1ubq')")
        name: Optional name for the output file (auto-generated if None)
        width: Image width in pixels
        height: Image height in pixels
        ray: Whether to ray-trace (slower but prettier)
        port: PyMOL socket port

    Returns:
        Path to the saved image file
    """
    output_path = generate_filename(name)

    # Build the full command sequence
    # IMPORTANT: cmd.png() with width/height parameters causes a PyMOL bug where
    # the view matrix Z-distance becomes corrupted after multiple cycles of
    # reinitialize + fetch + png. The Z-distance grows exponentially from ~120 to
    # ~50000+ after just 3-4 cycles, causing the view to zoom out into invisibility.
    #
    # The fix: ALWAYS use cmd.ray(width, height) before cmd.png(path) WITHOUT
    # dimensions in the png call. The ray() command renders to an offscreen buffer
    # without touching the viewport, preventing the corruption.

    render_cmd = f"cmd.ray({width}, {height})"
    png_cmd = f'cmd.png(r"{output_path}")'

    full_code = f"""
{commands}

# Render and save the image
{render_cmd}
{png_cmd}
print(f"Saved: {output_path}")
"""

    result = send_command(full_code, port=port, timeout=120.0)

    if result.get("status") == "success":
        # Wait briefly for file to be written
        time.sleep(0.2)
        if output_path.exists():
            return str(output_path)
        else:
            raise RuntimeError(f"Image was not saved to {output_path}")
    else:
        raise RuntimeError(f"PyMOL error: {result.get('error', 'Unknown error')}")


def quick_view(port: int = DEFAULT_PORT) -> str:
    """
    Take a quick snapshot of the current PyMOL view.

    Returns:
        Path to the saved image
    """
    return pymol_view("pass", name=None, port=port)
