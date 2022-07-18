import time
import logging
from flask.globals import current_app

logging.basicConfig(level=logging.INFO)

class DebugTimer:
    def __init__(self, text: str):
        self.text = text
        self._start_time = 0.
    def __enter__(self):
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, *exc_info):
        elapsed_time = time.perf_counter() - self._start_time
        current_app.logger.info(self.text.format(elapsed_time))
