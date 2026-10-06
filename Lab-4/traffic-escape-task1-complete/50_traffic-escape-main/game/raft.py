# game/raft.py

import pygame


class Raft:
    def __init__(
        self,
        y,
        width,
        screen_width,
        speed=2.5
    ):
        self.width = width
        self.screen_width = screen_width
        self.speed = speed
        self.height = 56

        self.rect = pygame.Rect(
            -width,
            y,
            width,
            self.height
        )

    def update(self):
        self.rect.x += self.speed

        if self.rect.left > self.screen_width:
            self.rect.right = 0

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (125, 80, 35),
            self.rect,
            border_radius=10
        )

        plank_h = 8

        for y in range(
            self.rect.top + 8,
            self.rect.bottom - 4,
            14
        ):
            pygame.draw.rect(
                screen,
                (170, 115, 55),
                pygame.Rect(
                    self.rect.x + 8,
                    y,
                    self.rect.width - 16,
                    plank_h
                ),
                border_radius=3
            )