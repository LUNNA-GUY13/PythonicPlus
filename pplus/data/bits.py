import struct

class BitStore:
    """
    The Pythonic+ Low-Level Data Controller.
    
    A high-performance wrapper for bit-level manipulation, extraction, 
    and hardware-aligned data conversion. Designed to bridge the gap 
    between Python's arbitrary-precision integers and fixed-width 
    hardware registers.

    Usage:
        >>> register = BitStore(0xDEADBEEF, width=32)
        >>> print(register[0:8])  # Extract first byte
        >>> register.rotate_left(4)
    """

    __slots__ = ['value', 'width', 'mask']

    def __init__(self, value: int = 0, width: int = 32):
        """
        Initialize the store with a value and a fixed bit-width.

        Args:
            value (int): Initial integer value.
            width (int): Target register width (8, 16, 32, 64, etc.)
        """
        self.width = width
        self.mask = (1 << width) - 1
        self.value = value & self.mask

    def __getitem__(self, key):
        """
        Slice-based bit extraction.
        
        Example:
            store[0:4] returns the 4 least significant bits.
        """
        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or self.width
            length = stop - start
            mask = (1 << length) - 1
            return (self.value >> start) & mask
        return (self.value >> key) & 1

    def rotate_left(self, n: int):
        """
        Circular bitwise left shift (ROL).
        
        Args:
            n (int): Number of positions to rotate.
        """
        n %= self.width
        self.value = ((self.value << n) | (self.value >> (self.width - n))) & self.mask

    def rotate_right(self, n: int):
        """
        Circular bitwise right shift (ROR).
        
        Args:
            n (int): Number of positions to rotate.
        """
        n %= self.width
        self.value = ((self.value >> n) | (self.value << (self.width - n))) & self.mask

    def to_float(self) -> float:
        """
        Cast the current bit pattern to an IEEE 754 float.
        (Requires width to be 32 or 64).
        """
        fmt = 'f' if self.width == 32 else 'd'
        pack_fmt = 'I' if self.width == 32 else 'Q'
        try:
            return struct.unpack(fmt, struct.pack(pack_fmt, self.value))[0]
        except Exception:
            return 0.0

    def __repr__(self) -> str:
        """
        Professional diagnostic string showing Hex, Dec, and Binary.
        """
        b_str = bin(self.value)[2:].zfill(self.width)
        return f"BitStore(Hex: {hex(self.value)}, Dec: {self.value}, Bin: {b_str})"