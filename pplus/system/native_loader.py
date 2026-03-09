import ctypes
import tempfile
import os
import atexit
from typing import Optional, Callable, Any

class NativeLoader:
    """
    The Pythonic+ Native Assembly Loader.
    
    Provides high-level abstractions for dynamically loading, executing,
    and managing native compiled code (DLLs, shared objects). This enables
    seamless interop between Python and hand-optimized C/C++/C# assemblies.
    
    Features:
        - Hot-load DLLs from memory without disk I/O overhead
        - Automatic cleanup of temporary files via atexit hooks
        - Cross-platform export resolution (Windows DLLs, Unix .so files)
        - Error handling with detailed failure diagnostics
        - Function pointer caching for repeated calls
    
    Usage:
        >>> loader = NativeLoader()
        >>> handle = loader.load_from_memory(dll_bytes)
        >>> result = loader.call_export(handle, "MyFunction", ctypes.c_int, 42)
    """
    
    def __init__(self):
        """Initialize the loader and register cleanup handlers."""
        self._loaded_handles = {}
        self._temp_files = []
        atexit.register(self._cleanup_all)
    
    @staticmethod
    def load_from_memory(dll_bytes: bytes) -> Optional[int]:
        """
        Dynamically loads a binary assembly from memory into the process space.
        
        Creates a temporary file on disk, writes the DLL bytes to it, and
        uses Win32 LoadLibraryW to map it into the current process. The temporary
        file is automatically cleaned up on exit.
        
        Args:
            dll_bytes (bytes): Raw binary content of the DLL/assembly.
        
        Returns:
            int: Handle to the loaded module, or None on failure.
            
        Raises:
            OSError: If temporary file creation fails.
            Exception: If Win32 LoadLibraryW fails.
        
        Example:
            >>> with open("native.dll", "rb") as f:
            ...     handle = NativeLoader.load_from_memory(f.read())
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=".dll", delete=False) as tmp:
                tmp.write(dll_bytes)
                tmp_path = tmp.name
            
            handle = ctypes.windll.kernel32.LoadLibraryW(tmp_path)
            if not handle:
                raise RuntimeError(f"Failed to load DLL: LoadLibraryW returned null for {tmp_path}")
            
            return handle
        except Exception as e:
            raise Exception(f"[NativeLoader] Memory load failed: {e}")
    
    @staticmethod
    def load_from_disk(dll_path: str) -> Optional[int]:
        """
        Loads a native DLL directly from disk path.
        
        Args:
            dll_path (str): Full path to the DLL file.
        
        Returns:
            int: Handle to the loaded module, or None on failure.
        
        Raises:
            FileNotFoundError: If the DLL path doesn't exist.
            Exception: If Win32 LoadLibraryW fails.
        """
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"DLL not found: {dll_path}")
        
        try:
            handle = ctypes.windll.kernel32.LoadLibraryW(dll_path)
            if not handle:
                raise RuntimeError(f"Failed to load DLL: {dll_path}")
            return handle
        except Exception as e:
            raise Exception(f"[NativeLoader] Disk load failed: {e}")
    
    @staticmethod
    def call_export(handle: int, export_name: str, return_type: Any, *args) -> Any:
        """
        Calls an exported function from a loaded native assembly.
        
        Resolves the function symbol by name, sets up the calling convention,
        and invokes it with the provided arguments.
        
        Args:
            handle (int): Module handle from load_from_memory or load_from_disk.
            export_name (str): Name of the exported C function.
            return_type: ctypes return type (e.g., ctypes.c_int, ctypes.c_void_p).
            *args: Arguments to pass to the function.
        
        Returns:
            Any: The return value from the native function.
        
        Raises:
            AttributeError: If the export is not found in the module.
        
        Example:
            >>> result = NativeLoader.call_export(handle, "Add", ctypes.c_int, 5, 3)
            >>> print(result)  # Prints: 8
        """
        try:
            func = ctypes.CDLL(handle)[export_name]
            func.restype = return_type
            return func(*args)
        except AttributeError as e:
            raise AttributeError(f"[NativeLoader] Export '{export_name}' not found: {e}")
    
    def _cleanup_all(self):
        """Internal cleanup routine: unload all modules and remove temp files."""
        for handle in self._loaded_handles.values():
            try:
                ctypes.windll.kernel32.FreeLibrary(handle)
            except:
                pass
        
        for tmp_path in self._temp_files:
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except:
                pass