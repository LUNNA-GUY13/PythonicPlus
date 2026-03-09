import time

def superloop(iterable, name="Task", max_retries=3, on_error=None):
    """
    Resilient iterator with built-in error handling and retry logic.
    
    Yields items from an iterable while catching and recovering from failures.
    If an item fails, it's automatically retried up to max_retries times before
    being skipped or passed to the error handler.
    
    Args:
        iterable: The sequence to iterate over.
        name (str): Task name for progress display.
        max_retries (int): Number of retry attempts per item.
        on_error (callable): Optional callback for handling failures: on_error(item, error, attempt).
    
    Yields:
        tuple: (item, success: bool, error: Exception or None)
    """
    total = len(iterable)
    start_time = time.time()
    failures = []
    
    for i, item in enumerate(iterable):
        success = False
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                yield (item, True, None)
                success = True
                break
            except Exception as e:
                last_error = e
                if on_error:
                    on_error(item, e, attempt + 1)
                if attempt < max_retries:
                    time.sleep(0.1 * (attempt + 1))
        
        if not success:
            failures.append((item, last_error))
            yield (item, False, last_error)
        
        percent = ((i + 1) / total) * 100
        elapsed = time.time() - start_time
        status = "✓" if success else "✗"
        print(f"\r [{name}] {status} {percent:>5.1f}% | Elapsed: {elapsed:.2f}s | Failures: {len(failures)}", end="")
