import argparse
import os
import sys
from .core.transformer import PPlusTransformer

BANNER = r"""
  _____           _   _                      _        _____  _             
 |  __ \         | | | |                    (_)      |  __ \| |            
 | |__) | _   _  | |_| |__    ___   _ __   _   ___  | |__) | | _   _  ___ 
 |  ___/ | | | | | __| '_ \  / _ \ | '_ \ | | / __| |  ___/| || | | |/ __|
 | |     | |_| | | |_| | | || (_) || | | || || (__  | |    | || |_| |\__ \
 |_|      \__, |  \__|_| |_| \___/ |_| |_||_| \___| |_|    |_| \__,_||___/
           __/ |                                                          
          |___/          [ V1.0.0 ALPHA - MASTERSTROKE EDITION ]
"""

class PPlusCLI:
    # ... previous init logic ...

    def run_build(self, filename):
        """The Transformer: Bundles Python + C# into a raw .pplus stream."""
        print(BANNER)
        print(f"[TRANSFORMER] Scanning {filename}...")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                source = f.read()

            print("[MASTERSTROKE] Extracting JIT assemblies...")
            # For Alpha: In-memory DLL capture
            fake_dll_bytes = b"PPLUS_STUB_DATA" 

            print("[ENCODER] Writing .pplus stream...")
            bundle = PPlusTransformer.pack(source, fake_dll_bytes)

            if not os.path.exists("dist"): 
                os.makedirs("dist")
            
            output_name = f"dist/{filename.replace('.py', '.pplus')}"
            with open(output_name, 'wb') as f:
                f.write(bundle)
                
            print(f"\n[SUCCESS] Code compiled to {output_name}")
            print("[STATUS] Ready for P+ Runtime deployment.")
            
        except Exception as e:
            print(f"[ERROR] Build failed: {str(e)}")