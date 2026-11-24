# ROV Ground Control Station

**AAST Triton ROVs – Software Training | Phase 1: Foundation and Input**

## Project Overview

This project implements the foundation of a Ground Control Station (GCS) for an ROV. Phase 1 focuses on building a headless software structure for configuration management, event handling, and operator input.

## Phase 1 Features

- **Configuration Manager:** Loads settings from `config/settings.json`.
- **Event System:** Implements an Event class and EventBus for event communication.
- **Keyboard Input:** Handles keyboard input.
- **Controller Input:** Handles game controller input using Pygame.
- **Input Manager:** Combines keyboard and controller inputs and publishes `input_updated` events.
- **Main Application:** Starts the system components and handles clean shutdown.

**Note:** Networking is not included in Phase 1.

## Project Structure

```text
ROV-GCS/
│   main.py
│   .gitignore
│
├── config/
│   └── settings.json
│
├── Core/
│   ├── config_manager.py
│   ├── controller.py
│   ├── events.py
│   ├── event_bus.py
│   ├── input_manager.py
│   ├── keyboard.py
│   ├── profiles.py
│   └── __init__.py
│
└── tests/
    ├── test_config_manager.py
    ├── test_controller.py
    ├── test_event_bus.py
    ├── test_input_manager.py
    ├── test_keyboard.py
    ├── test_main.py
    └── test_profiles.py
```

## Requirements

- Python
- pygame-ce
- pytest

## Installation

Install the required packages:

```bash
py -m pip install pygame-ce pytest
```

## Running the Application

Run the main application:

```bash
py main.py
```

Press `Ctrl + C` to stop the application safely.

## Running Tests

Run the complete test suite:

```bash
py -m pytest -v
```

Latest verification: **29 tests passed**.

## Project Status

Phase 1 – Foundation and Input: Implemented and tested.