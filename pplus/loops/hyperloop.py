import time
import json
import os
from ..core.project import Project
from ..core.turbo import TurboEngine
from ..system.hardware import HardwareRecon

def hyperloop(iterable, name="Process", checkpoint=True):
    project = Project()
    hw = HardwareRecon()
    
    _time = time.time
    _print = print
    
    total = len(iterable)
    start_all = _time()
    last_tick = start_all
    
    start_index = 0
    checkpoint_file = f".pplus_checkpoint_{name}.json"
    
    if checkpoint and os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                saved_data = json.load(f)
                start_index = saved_data.get("last_index", 0)
                if start_index > 0:
                    print(f"♻️  [HyperLoop] Resuming {name} from item {start_index}...")
        except: pass

    _print(f"[HyperLoop] Starting {name} on {hw.arch}...")

    # Slice the iterable if we are resuming
    current_iterable = iterable[start_index:] if start_index < total else []

    with TurboEngine.throttle_gc():
        for i, item in enumerate(current_iterable):
            actual_index = i + start_index
            yield item
            
            # Physics & Metrics
            now = _time()
            delta = now - last_tick
            total_elapsed = now - start_all
            items_per_sec = (actual_index + 1) / total_elapsed
            percent = ((actual_index + 1) / total) * 100
            
            _print(f"\r   {percent:>5.1f}% | {items_per_sec:>6.2f} it/s | Δ: {delta:.4f}s | {name}", end="")
            
            if checkpoint and actual_index % 10 == 0:
                with open(checkpoint_file, 'w') as f:
                    json.dump({"last_index": actual_index, "timestamp": now}, f)
            
            last_tick = now
        
    if checkpoint and os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)
        
    print(f"\n{name} Complete in {total_elapsed:.2f}s.")