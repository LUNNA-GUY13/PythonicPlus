from .core.project import Project
from .system.bridge import NativeBridge
from .system.hardware import HardwareRecon
from .system.logger import AutoLogger
from .data.bits import BitList
from .data.serializer import UniversalData
from .loops.superloop import superloop
from .loops.hyperloop import hyperloop

# Initialize the Core HQ Instances
project = Project()
bridge = NativeBridge()
hardware = HardwareRecon()
data = UniversalData()
logger = None

# Global Logger Initialization
if project.is_enabled("auto_logger"):
    # Passing hardware.report() gives the logger full context on the crash site
    logger = AutoLogger(project.name, hardware.report())

# Exporting the API
# Fixed the missing quote on "BitStore" and matched it to your import
__all__ = [
    "bridge", 
    "BitList", 
    "project", 
    "hardware", 
    "data", 
    "superloop", 
    "hyperloop",
    "logger"
]