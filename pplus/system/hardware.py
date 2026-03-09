import os
import platform
import subprocess

class HardwareRecon:
    """
    The Pythonic+ Environment Profiler.
    
    Identifies the underlying hardware architecture, OS kernel, and 
    virtualization status. This module is used to calibrate the 
    HyperLoop and prepare for low-level JIT optimizations.

    Usage:
        >>> from pplus.system.hardware import HardwareRecon
        >>> recon = HardwareRecon()
        >>> print(recon.report())
    """

    def __init__(self):
        """
        Initialize hardware discovery and cache system signatures.
        """
        self.os_name = os.name
        self.system = platform.system()
        self.arch = platform.machine()
        self.cores = os.cpu_count() or 1
        
        self.is_arm = 'arm' in self.arch.lower() or 'aarch64' in self.arch.lower()
        self.is_64bit = '64' in platform.architecture()[0]
        
        self.is_vm = self._check_virtualization()

    def _check_virtualization(self) -> bool:
        """
        Detects if the code is running inside a Virtual Machine or Sandbox.
        
        Returns:
            bool: True if common VM signatures (VMware, VirtualBox, Hyper-V) are found.
        """
        vm_indicators = ['virtual', 'vbox', 'vmware', 'qemu', 'hyper-v']
        try:
            # On Windows, we can check the system manufacturer via shell
            if self.os_name == 'nt':
                output = subprocess.check_output('wmic baseboard get manufacturer', shell=True).decode().lower()
                return any(vendor in output for vendor in vm_indicators)
        except:
            pass
        return False

    def get_thermal_status(self) -> str:
        """
        Place-holder for future JIT-Safe thermal throttling logic.
        """
        return "Optimal" # To be expanded with native C# calls later

    def report(self) -> str:
        """
        Generates a standardized hardware signature string.

        Returns:
            str: A pipe-delimited profile of the current machine state.
        """
        vm_status = "[VM]" if self.is_vm else "[NATIVE]"
        arch_type = "ARM-64" if self.is_arm else f"x86-{self.arch}"
        
        return (
            f"OS: {self.system} ({self.os_name}) | "
            f"Arch: {arch_type} | "
            f"Cores: {self.cores} | "
            f"Env: {vm_status}"
        )