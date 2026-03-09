import ctypes
import os
import sys

class NativeBridge:
    """
    The Pythonic+ Windows Native Interface.
    
    Provides direct access to Win32 API calls via ctypes. This allows the HQ 
    to trigger system-level UI, notifications, and terminal manipulations 
    without external dependencies.

    Note:
        Fallback logic is provided for POSIX systems to ensure cross-platform 
        import stability.
    """

    def __init__(self):
        """
        Initialize the bridge and detect the host environment.
        """
        self.is_windows = os.name == 'nt'
        if self.is_windows:
            self.user32 = ctypes.windll.user32
            self.kernel32 = ctypes.windll.kernel32
            self.shell32 = ctypes.windll.shell32

    def alert(self, title: str, message: str, icon: int = 0x40):
        """
        Trigger a native Windows MessageBox.
        
        Args:
            title (str): The window header.
            message (str): The body text.
            icon (int): 0x40 (Info), 0x30 (Warning), 0x10 (Error).
        """
        if self.is_windows:
            self.user32.MessageBoxW(0, message, title, icon | 0x1)
        else:
            print(f"[{title}] {message}")

    def flash_window(self, count: int = 5):
        """
        Makes the terminal taskbar icon flash to alert the user.
        """
        if self.is_windows:
            hwnd = self.kernel32.GetConsoleWindow()
            if hwnd:
                for _ in range(count):
                    self.user32.FlashWindow(hwnd, True)
                    import time
                    time.sleep(0.5)

    def set_console_title(self, title: str):
        """
        Updates the terminal window title dynamically.
        """
        if self.is_windows:
            self.kernel32.SetConsoleTitleW(title)
        else:
            sys.stdout.write(f"\x1b]2;{title}\x07")

    def ghost_toast(self, title: str, message: str):
        """
        A non-blocking system notification. 
        Currently uses a fallback, but prepared for Shell_NotifyIcon.
        """
        print(f"\n[*] NOTIFICATION: {title} -> {message}")