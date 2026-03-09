import json
import os

class Project:
    def __init__(self):
        self.config = self._load()
        self.name = self.config.get("project_name", "Untitled")

    def _load(self):
        if os.path.exists(".pyproj"):
            try:
               
                with open(".pyproj", "r", encoding="utf-8-sig") as f:
                    content = f.read().strip()
                    if not content:
                        return {"toggles": {}}
                    return json.loads(content)
            except Exception as e:
                print(f" Warning: Could not parse .pyproj: {e}")
                return {"toggles": {}}
        return {"toggles": {}}

    def is_enabled(self, feature):
        return self.config.get("toggles", {}).get(feature, False)