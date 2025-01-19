"""Performance monitoring utilities."""

import time
from functools import wraps
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)


def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure function execution time."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.debug(f"{func.__name__} took {end - start:.2f} seconds")
        return result

    return wrapper
