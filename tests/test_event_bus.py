
import threading
import time

from Core.events import Event
from Core.event_bus import EventBus


def test_event_bus_publish_subscribe():
    bus = EventBus()

    received_events = []
    event_received = threading.Event()

    def handle_event(event):
        received_events.append(event)
        event_received.set()

    bus.subscribe("test_event", handle_event)
    bus.start()

    try:
        event = Event(
            event_type="test_event",
            data={"message": "Hello ROV"}
        )

        bus.publish(event)

        assert event_received.wait(timeout=2)
        assert received_events[0].data["message"] == "Hello ROV"

    finally:
        bus.stop()


def test_event_bus_receives_multiple_events():
    bus = EventBus()
    received = []
    all_received = threading.Event()

    def handle_event(event):
        received.append(event)
        if len(received) == 3:
            all_received.set()

    bus.subscribe("test", handle_event)
    bus.start()

    try:
        for i in range(3):
            bus.publish(Event("test", {"number": i}))

        assert all_received.wait(timeout=2)
        assert len(received) == 3

    finally:
        bus.stop()


def test_event_bus_handles_callback_exception():
    bus = EventBus()
    received = threading.Event()

    def broken_callback(event):
        raise ValueError("Test error")

    def working_callback(event):
        received.set()

    bus.subscribe("test", broken_callback)
    bus.subscribe("test", working_callback)
    bus.start()

    try:
        bus.publish(Event("test"))

        assert received.wait(timeout=2)

    finally:
        bus.stop()


def test_event_bus_stop_and_restart():
    bus = EventBus()

    first_received = threading.Event()
    second_received = threading.Event()

    bus.subscribe(
        "first",
        lambda event: first_received.set()
    )

    bus.subscribe(
        "second",
        lambda event: second_received.set()
    )

    bus.start()
    bus.publish(Event("first"))

    assert first_received.wait(timeout=2)

    bus.stop()
    bus.start()

    try:
        bus.publish(Event("second"))
        assert second_received.wait(timeout=2)

    finally:
        bus.stop()
