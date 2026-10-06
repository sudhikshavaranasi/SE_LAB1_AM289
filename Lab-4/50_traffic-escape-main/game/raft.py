import pygame


class Raft:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        screen_width,
        speed=2.5
    ):
        self.x = float(x)
        self.y = float(y)

        self.width = width
        self.height = height

        self.screen_width = screen_width
        self.speed = float(speed)

        # Amount moved during the current frame.
        self.last_dx = 0

        # The collision rectangle is exactly the same size and
        # position as the visible raft.
        self.rect = pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def update(self):
        old_x = self.x

        # Continuous horizontal movement.
        self.x += self.speed

        # Wrap around to the left once the raft completely
        # leaves the right side of the screen.
        if self.x >= self.screen_width:
            self.x = -float(self.width)

        self.last_dx = round(
            self.x - old_x
        )

        # Keep collision rectangle synchronized with the
        # visible raft position.
        self.rect.x = int(round(self.x))
        self.rect.y = int(round(self.y))

    def draw(self, screen):
        # Visible raft uses the exact same rectangle used
        # for collision detection.
        pygame.draw.rect(
            screen,
            (125, 80, 35),
            self.rect,
            border_radius=10
        )

        # Wooden planks.
        plank_height = 8

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
                    plank_height
                ),
                border_radius=3
            )