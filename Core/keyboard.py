import pygame


class KeyboardInput:
    def __init__(self):
        pygame.init()
        self.pressed_keys = set()

    def update(self):
        events = pygame.event.get([
            pygame.KEYDOWN,
            pygame.KEYUP
        ])

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)

            elif event.type == pygame.KEYUP:
                self.pressed_keys.discard(event.key)

        return self.pressed_keys

    def is_pressed(self, key):
        return key in self.pressed_keys