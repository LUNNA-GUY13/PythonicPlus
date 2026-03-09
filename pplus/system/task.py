import asyncio
import threading

class Task:
    @staticmethod
    def run(coro):
        """Entry point for executing async coroutines."""
        return asyncio.run(coro)

    @staticmethod
    def fire_and_forget(func, *args):
        """Background execution without blocking."""
        thread = threading.Thread(target=func, args=args, daemon=True)
        thread.start()
        return thread

    @staticmethod
    def sleep(seconds):
        """Sleep for the specified duration, handling both async and sync contexts."""
        import time
        try:
            loop = asyncio.get_running_loop()
            return asyncio.sleep(seconds)
        except RuntimeError:
            time.sleep(seconds)