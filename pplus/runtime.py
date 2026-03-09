import sys
import types
from .core.transformer import PPlusTransformer

class PPlusRuntime:
    """
    The Pythonic+ Execution Environment.
    Handles the injection of extracted source into the CPython VM.
    """

    @staticmethod
    def run_bundle(blob: bytes):
        """
        Unpacks the .pplus stream and executes the embedded logic.
        """
        print("[RUNTIME] Unpacking binary stream...")
        dll_data, python_source = PPlusTransformer.unpack(blob)

        # 1. Prepare the Execution Context
        # We create a fresh module-like namespace for the script
        script_globals = {
            "__name__": "__main__",
            "__file__": "memory_bundle.pplus",
            "__pplus_dll__": dll_data  # Pass the DLL data for the JIT to find
        }

        print("[RUNTIME] Initializing Pythonic+ Logic...")
        try:
            # 2. Execution
            # This is where the Python source comes alive
            exec(python_source, script_globals)
        except Exception as e:
            print(f"\n[CRASH] Runtime execution failed: {e}")
            import traceback
            traceback.print_exc()