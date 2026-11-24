
import queue
import threading
import logging

from collections import defaultdict
from typing import Callable

from .events import Event


class EventBus:

    def __init__(self):
        self._queue = queue.Queue()
        self._subscribers = defaultdict(list)
        self._lock = threading.Lock()
        self._running = threading.Event()
        self._thread = None

    def subscribe(self, event_type: str, callback: Callable):
        with self._lock:
            self._subscribers[event_type].append(callback)

    def publish(self, event: Event):
        self._queue.put(event)

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return

        self._running.set()

        self._thread = threading.Thread(
            target=self._process_events,
            daemon=True
        )

        self._thread.start()

    def _process_events(self):
        while self._running.is_set():
            try:
                event = self._queue.get(timeout=0.1)

            except queue.Empty:
                continue

            try:
                with self._lock:
                    callbacks = list(
                        self._subscribers.get(event.event_type, [])
                    )

                for callback in callbacks:
                    try:
                        callback(event)
                    except Exception:
                        logging.exception("Error processing event")

            finally:
                self._queue.task_done()

    def stop(self):
        self._running.clear()

        if self._thread is not None:
            self._thread.join(timeout=2)

        self._thread = None
