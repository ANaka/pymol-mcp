"""
PyMOL Session Manager

Provides reliable session lifecycle management:
- Launch PyMOL with plugin
- Health checks
- Graceful and forced termination
- Crash detection and recovery
"""

import os
import signal
import subprocess
import time
from pathlib import Path

from claudemol.connection import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    PyMOLConnection,
    find_pymol_command,
    get_plugin_path,
)


class PyMOLSession:
    """
    Manages a PyMOL session with health monitoring and recovery.

    Usage:
        session = PyMOLSession()
        session.start()

        # Use the connection
        result = session.execute("cmd.fetch('1ubq')")

        # Check health
        if not session.is_healthy():
            session.recover()

        # Clean up
        session.stop()
    """

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.process = None
        self.connection = None
        self._we_launched = False  # Track if we started PyMOL

    @property
    def is_running(self):
        """Check if we have a PyMOL process that's still alive."""
        if self.process is None:
            return False
        return self.process.poll() is None

    @property
    def is_connected(self):
        """Check if we have a socket connection."""
        return self.connection is not None and self.connection.is_connected()

    def is_healthy(self):
        """
        Check if PyMOL is responsive by executing a trivial command.

        Returns True if we can communicate with PyMOL.
        """
        if not self.is_connected:
            return False
        try:
            result = self.connection.execute("print('ping')")
            return "ping" in result
        except Exception:
            return False

    def start(self, timeout=15.0):
        """
        Start PyMOL or connect to existing instance.

        Args:
            timeout: How long to wait for PyMOL to be ready

        Returns:
            True if connected successfully
        """
        self.connection = PyMOLConnection(self.host, self.port)

        # Try connecting to existing instance first
        try:
            self.connection.connect(timeout=2.0)
            self._we_launched = False
            return True
        except ConnectionError:
            pass

        # Launch new instance
        pymol_cmd = find_pymol_command()
        if not pymol_cmd:
            raise RuntimeError(
                "PyMOL not found. Run: claudemol setup"
            )

        # Check if plugin is configured in pymolrc (don't double-load)
        pymolrc_path = Path.home() / ".pymolrc"
        plugin_in_pymolrc = False
        if pymolrc_path.exists():
            content = pymolrc_path.read_text()
            if "claude_socket_plugin" in content or "claudemol" in content:
                plugin_in_pymolrc = True

        # Build command - only add plugin if not in pymolrc
        cmd_args = list(pymol_cmd)
        if not plugin_in_pymolrc:
            plugin_path = get_plugin_path()
            if not plugin_path.exists():
                raise RuntimeError(f"Plugin not found: {plugin_path}")
            cmd_args += ["-d", f"run {plugin_path}"]

        # Launch PyMOL
        self.process = subprocess.Popen(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self._we_launched = True

        # Wait for socket to become available
        start = time.time()
        while time.time() - start < timeout:
            try:
                self.connection.connect(timeout=1.0)
                return True
            except ConnectionError:
                if not self.is_running:
                    # Process died during startup
                    stdout, stderr = self.process.communicate(timeout=1)
                    raise RuntimeError(
                        f"PyMOL exited during startup.\n"
                        f"stdout: {stdout.decode()}\n"
                        f"stderr: {stderr.decode()}"
                    )
                time.sleep(0.5)

        # Timeout - kill the process
        self._kill_process()
        raise TimeoutError(f"PyMOL socket not available after {timeout}s")

    def stop(self, graceful_timeout=5.0):
        """
        Stop PyMOL session.

        Args:
            graceful_timeout: Time to wait for graceful shutdown before force kill
        """
        # Disconnect socket
        if self.connection:
            self.connection.disconnect()
            self.connection = None

        # Only kill process if we launched it
        if self._we_launched and self.process:
            self._kill_process(graceful_timeout)

    def _kill_process(self, graceful_timeout=5.0):
        """Kill the PyMOL process."""
        if not self.process:
            return

        # Try graceful termination first
        try:
            self.process.terminate()
            self.process.wait(timeout=graceful_timeout)
        except subprocess.TimeoutExpired:
            # Force kill
            self.process.kill()
            self.process.wait(timeout=2.0)
        except Exception:
            pass

        self.process = None
        self._we_launched = False

    def recover(self, timeout=15.0):
        """
        Recover from a crashed or unresponsive PyMOL.

        This will:
        1. Kill any stale process
        2. Disconnect stale socket
        3. Start fresh

        Returns:
            True if recovery successful
        """
        # Clean up
        if self.connection:
            self.connection.disconnect()
            self.connection = None

        if self._we_launched:
            self._kill_process(graceful_timeout=2.0)

        # Also try to kill any orphaned PyMOL processes on our port
        self._kill_processes_on_port()

        # Brief pause to let OS clean up
        time.sleep(0.5)

        # Start fresh
        return self.start(timeout=timeout)

    def _kill_processes_on_port(self):
        """Kill any processes listening on our port (Linux/macOS)."""
        try:
            # Find PIDs using our port
            result = subprocess.run(
                ["lsof", "-ti", f":{self.port}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.stdout.strip():
                pids = result.stdout.strip().split("\n")
                for pid in pids:
                    try:
                        os.kill(int(pid), signal.SIGKILL)
                    except (ValueError, ProcessLookupError, PermissionError):
                        pass
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    def execute(self, code, auto_recover=True):
        """
        Execute code in PyMOL with optional auto-recovery.

        Args:
            code: Python code to execute in PyMOL
            auto_recover: If True, attempt recovery on failure

        Returns:
            Output from PyMOL
        """
        try:
            if not self.is_connected:
                if auto_recover:
                    self.recover()
                else:
                    raise ConnectionError("Not connected to PyMOL")

            return self.connection.execute(code)

        except (ConnectionError, TimeoutError):
            if auto_recover:
                self.recover()
                return self.connection.execute(code)
            raise

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


# Convenience: global session instance
_session = None


def get_session():
    """Get or create the global PyMOL session."""
    global _session
    if _session is None:
        _session = PyMOLSession()
    return _session


def ensure_running():
    """Ensure PyMOL is running and connected."""
    session = get_session()
    if not session.is_healthy():
        session.start()
    return session


def stop_pymol():
    """Stop the global PyMOL session."""
    global _session
    if _session:
        _session.stop()
        _session = None
