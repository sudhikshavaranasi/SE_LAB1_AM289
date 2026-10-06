import pygame
import random


LANE_W = 80

COLORS = [
    (220, 60, 60),
    (220, 140, 40),
    (140, 60, 180),
    (60, 180, 80),
    (180, 180, 40),
    (60, 80, 200)
]


class Car:
    def __init__(
        self,
        lane_x,
        y,
        direction,
        speed
    ):
        self.rect = pygame.Rect(
            lane_x + 10,
            y,
            60,
            80
        )

        self.direction = direction
        self.speed = speed
        self.color = random.choice(
            COLORS
        )

    def update(self):
        self.rect.y += (
            self.direction
            * self.speed
        )

    def off_screen(self, height):
        return (
            self.rect.top > height + 100
            or self.rect.bottom < -100
        )

    def draw(
        self,
        screen,
        night=False
    ):
        # ========================================================
        # CAR BODY
        # ========================================================

        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=8
        )

        # Windows.
        pygame.draw.rect(
            screen,
            (180, 220, 240),
            pygame.Rect(
                self.rect.x + 8,
                self.rect.y + 10,
                44,
                22
            ),
            border_radius=4
        )

        # ========================================================
        # WHEELS
        # ========================================================

        for wx in [
            self.rect.x + 6,
            self.rect.right - 16
        ]:
            for wy in [
                self.rect.y + 4,
                self.rect.bottom - 16
            ]:
                pygame.draw.rect(
                    screen,
                    (30, 30, 30),
                    pygame.Rect(
                        wx,
                        wy,
                        10,
                        12
                    ),
                    border_radius=3
                )

        # ========================================================
        # NIGHT HEADLIGHTS
        # ========================================================

        if night:
            self.draw_headlights(
                screen
            )

    def draw_headlights(
        self,
        screen
    ):
        """
        Draw headlights and longer light beams.

        Cars moving downward have their front at the bottom.
        Cars moving upward have their front at the top.
        """

        headlight_color = (
            255,
            245,
            180
        )

        beam_color = (
            255,
            245,
            190,
            45
        )

        if self.direction > 0:
            # Car is travelling downward.
            front_y = self.rect.bottom

            left_x = self.rect.x + 12
            right_x = self.rect.right - 22

            # Light beams extend ahead of the car.
            left_beam = [
                (
                    left_x,
                    front_y
                ),
                (
                    left_x - 16,
                    front_y + 90
                ),
                (
                    left_x + 18,
                    front_y + 90
                ),
                (
                    left_x + 8,
                    front_y
                )
            ]

            right_beam = [
                (
                    right_x,
                    front_y
                ),
                (
                    right_x - 8,
                    front_y + 90
                ),
                (
                    right_x + 26,
                    front_y + 90
                ),
                (
                    right_x + 8,
                    front_y
                )
            ]

            self._draw_transparent_polygon(
                screen,
                beam_color,
                left_beam
            )

            self._draw_transparent_polygon(
                screen,
                beam_color,
                right_beam
            )

            pygame.draw.rect(
                screen,
                headlight_color,
                pygame.Rect(
                    left_x,
                    front_y - 3,
                    10,
                    7
                ),
                border_radius=2
            )

            pygame.draw.rect(
                screen,
                headlight_color,
                pygame.Rect(
                    right_x,
                    front_y - 3,
                    10,
                    7
                ),
                border_radius=2
            )

        else:
            # Car is travelling upward.
            front_y = self.rect.top

            left_x = self.rect.x + 12
            right_x = self.rect.right - 22

            left_beam = [
                (
                    left_x,
                    front_y
                ),
                (
                    left_x - 16,
                    front_y - 90
                ),
                (
                    left_x + 18,
                    front_y - 90
                ),
                (
                    left_x + 8,
                    front_y
                )
            ]

            right_beam = [
                (
                    right_x,
                    front_y
                ),
                (
                    right_x - 8,
                    front_y - 90
                ),
                (
                    right_x + 26,
                    front_y - 90
                ),
                (
                    right_x + 8,
                    front_y
                )
            ]

            self._draw_transparent_polygon(
                screen,
                beam_color,
                left_beam
            )

            self._draw_transparent_polygon(
                screen,
                beam_color,
                right_beam
            )

            pygame.draw.rect(
                screen,
                headlight_color,
                pygame.Rect(
                    left_x,
                    front_y - 4,
                    10,
                    7
                ),
                border_radius=2
            )

            pygame.draw.rect(
                screen,
                headlight_color,
                pygame.Rect(
                    right_x,
                    front_y - 4,
                    10,
                    7
                ),
                border_radius=2
            )

    @staticmethod
    def _draw_transparent_polygon(
        screen,
        color,
        points
    ):
        """
        Draw a transparent light beam without adding
        any external dependency.
        """

        surface = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        pygame.draw.polygon(
            surface,
            color,
            points
        )

        screen.blit(
            surface,
            (0, 0)
        )


def make_car(
    lane_idx,
    height,
    speed
):
    x = lane_idx * LANE_W

    direction = (
        1
        if lane_idx % 2 == 0
        else -1
    )

    y = (
        -90
        if direction == 1
        else height + 10
    )

    return Car(
        x,
        y,
        direction,
        speed
    )