import functools
import logging
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])

class JoyBoyError(Exception):
    pass

class DatabaseError(JoyBoyError):
    pass

class ValidationError(JoyBoyError):
    pass

class NotFoundError(JoyBoyError):
    pass

class DuplicateError(JoyBoyError):
    pass

def handle_errors(reraise: bool = True, default: Any = None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                logger.error("Error in %s: %s", func.__qualname__, str(exc))
                if reraise:
                    raise
                return default
        return wrapper
    return decorator