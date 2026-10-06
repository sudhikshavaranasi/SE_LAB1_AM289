import pygame


class Raft:
    def __init__(
        self,
        y,
        width,
        height,
        screen_width,
        speed=2.5
    ):
        self.width = width
        self.height = height

        self.screen_width = screen_width
        self.speed = float(speed)

        # Start partially off-screen so the raft enters
        # the river naturally.
        self.rect = pygame.Rect(
            -width,
            y,
            width,
            height
        )

        self.last_dx = 0

    def update(self):
        old_x = self.rect.x

        self.rect.x += round(
            self.speed
        )

        # Wrap around.
        if self.rect.left >= self.screen_width:
            self.rect.right = 0

        self.last_dx = (
            self.rect.x - old_x
        )

    def draw(
        self,
        screen
    ):
        # The visible raft and collision rectangle
        # are exactly the same size.
        pygame.draw.rect(
            screen,
            (125, 80, 35),
            self.rect,
            border_radius=10
        )

        # Wooden planks.
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
                    8
                ),
                border_radius=3
            )