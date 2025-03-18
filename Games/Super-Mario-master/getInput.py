import sys

if sys.platform.startswith('win'):
    import msvcrt

    class _GetCh:
        def __call__(self):
            # Use msvcrt on Windows
            return msvcrt.getch().decode('utf-8')
else:
    import tty
    import termios

    class _GetCh:
        def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

# Expose a getch function that works on all systems.
getch = _GetCh()