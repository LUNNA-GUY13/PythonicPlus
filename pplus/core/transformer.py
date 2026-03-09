import struct
import base64

class PPlusTransformer:
    """
    The Pythonic+ Binary Encoder.
    
    Converts Python/C# hybrid logic into encrypted .pplus containers.
    This ensures integrity and provides a 'Single-File' deployment 
    strategy for native modules.
    """

    @staticmethod
    def pack(python_logic: str, compiled_dll_bytes: bytes) -> bytes:
        """
        Transforms raw source and DLL into a .pplus binary blob.
        
        Structure: [Header: 8b][DLL_Len: 4b][DLL_Data][Py_Logic]
        """
        header = b"PPLUS_V1"
        dll_len = len(compiled_dll_bytes)
        # We pack the length of the DLL so we know where it ends
        package = struct.pack(f"<8sI{dll_len}s", header, dll_len, compiled_dll_bytes)
        # Append the python logic as encoded string
        package += python_logic.encode('utf-8')
        return package

    @staticmethod
    def unpack(pplus_bytes: bytes):
        """Extracts the DLL and Logic for execution."""
        header, dll_len = struct.unpack("<8sI", pplus_bytes[:12])
        dll_data = pplus_bytes[12:12+dll_len]
        py_logic = pplus_bytes[12+dll_len:].decode('utf-8')
        return dll_data, py_logic