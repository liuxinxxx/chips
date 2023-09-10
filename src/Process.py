from collections.abc import Callable, Iterable, Mapping
from typing import Any
import threading

class Process(threading.Thread):
    def __init__(self, threadID, name) -> None:
        return NotImplementedError
