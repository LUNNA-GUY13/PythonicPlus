import json
import os
import xml.etree.ElementTree as ET
import configparser
import csv

class UniversalData:
    """
    The Pythonic+ Omni-Parser Engine.
    
    A unified interface designed to ingest structured data across standard, 
    legacy, and proprietary formats. This module utilizes 'Ghost Imports' 
    to maintain a zero-dependency footprint during static analysis while 
    providing deep support for modern config types.

    Supported Formats:
        - JSON, XML (Native)
        - INI, CSV (Standard Library)
        - .PPML (PythonicPlus Proprietary)
        - YAML, TOML (Dynamic Support)
    """

    @staticmethod
    def load(filepath: str) -> dict:
        """
        Global entry point for data ingestion. Detects format via extension.
        
        Args:
            filepath (str): Path to the target data file.
            
        Returns:
            dict: The parsed data payload or a structured error report.
        """
        if not os.path.exists(filepath): 
            return {"status": "error", "message": f"File not found: {filepath}"}
        
        ext = filepath.split('.')[-1].lower()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # --- 1. CORE WEB FORMATS ---
                if ext == 'json':
                    return json.load(f)
                
                elif ext == 'xml':
                    try:
                        tree = ET.parse(f)
                        root = tree.getroot()
                        return {root.tag: {c.tag: c.text for c in root}}
                    except ET.ParseError as e:
                        return {"status": "error", "message": f"XML Parse Error: {e}"}

                # --- 2. PYTHONIC+ PROPRIETARY (PPML) ---
                elif ext == 'ppml':
                    return UniversalData._parse_ppml(f.read())

                # --- 3. SYSTEM & LEGACY FORMATS ---
                elif ext == 'ini':
                    config = configparser.ConfigParser()
                    # We read the file pointer directly for efficiency
                    config.read_file(f)
                    return {s: dict(config.items(s)) for s in config.sections()}

                elif ext == 'csv':
                    f.seek(0) # Reset pointer for DictReader
                    reader = csv.DictReader(f)
                    return [row for row in reader]

                # --- 4. GHOST IMPORTS (DYNAMIC DEPENDENCIES) ---
                # This section prevents IDE 'Missing Import' warnings (Pylance/Pyright)
                elif ext in ['yaml', 'yml']:
                    try:
                        yaml_mod = __import__('yaml')
                        return yaml_mod.safe_load(f)
                    except ImportError: 
                        return {"status": "dependency_error", "message": "Run 'pip install pyyaml' for YAML support."}

                elif ext == 'toml':
                    # Priority 1: Python 3.11+ Native
                    try:
                        toml_mod = __import__('tomllib')
                        return toml_mod.loads(f.read())
                    except ImportError:
                        # Priority 2: External tomli library
                        try:
                            tomli_mod = __import__('tomli')
                            return tomli_mod.loads(f.read())
                        except ImportError:
                            return {"status": "dependency_error", "message": "TOML requires Python 3.11+ or 'pip install tomli'."}

        except Exception as global_err:
            return {"status": "critical_failure", "message": str(global_err)}

        return {"status": "error", "message": f"Unsupported file extension: {ext}"}

    @staticmethod
    def _parse_ppml(content: str) -> dict:
        """
        Internal Logic for PythonicPlus Markup Language (.ppml).
        Syntax: [Key] >> [Value] # [Comment]
        
        Args:
            content (str): The raw string content of the .ppml file.
            
        Returns:
            dict: Key-Value pairs extracted from the markup.
        """
        data = {}
        for line in content.splitlines():
            # Strip comments and whitespace
            clean_line = line.split('#')[0].strip()
            if '>>' in clean_line:
                key, val = clean_line.split('>>', 1)
                data[key.strip()] = val.strip()
        return data