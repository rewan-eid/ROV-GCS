
import pygame
from Core.keyboard import KeyboardInput


def test_keyboard_key_down():
    keyboard = KeyboardInput()

    pygame.event.post(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
    )

    keyboard.update()

    assert keyboard.is_pressed(pygame.K_w)


def test_keyboard_key_up():
    keyboard = KeyboardInput()

    keyboard.pressed_keys.add(pygame.K_w)

    pygame.event.post(
        pygame.event.Event(pygame.KEYUP, key=pygame.K_w)
    )

    keyboard.update()

    assert not keyboard.is_pressed(pygame.K_w)
