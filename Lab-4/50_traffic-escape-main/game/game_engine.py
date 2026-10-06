import pygame
import random

from game.player import Player, LANE_W
from game.traffic import make_car
from game.raft import Raft


LANES = 8
WIDTH = LANES * LANE_W
HEIGHT = 600
FPS = 60

BG = (60, 60, 60)

# Dedicated moving-raft lane.
# It is exactly one lane high, so it is reachable using the
# existing 8-pixel forward/backward movement.
RIVER_TOP = 260
RIVER_BOTTOM = 340

RAFT_Y = RIVER_TOP + 12
RAFT_WIDTH = 260
RAFT_HEIGHT = 56


class GameEngine:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Escape")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "monospace",
            20,
            bold=True
        )

        self.big_font = pygame.font.SysFont(
            "monospace",
            44,
            bold=True
        )

        self.reset()

    def reset(self):
        self.start_x = WIDTH // 2
        self.start_y = HEIGHT - 80

        self.player = Player(
            self.start_x,
            self.start_y
        )

        self.cars = []

        self.timer = 0
        self.spawn_interval = 50
        self.speed = 3

        self.score = 0

        # Existing Task 1 lives system.
        self.lives = 3

        self.game_over = False
        self.won = False

        # Prevent immediate repeated collision after respawn.
        self.hit_cooldown = 0

        # Start the raft visibly inside the river.
        # This is important: the old implementation started the raft
        # completely off-screen, making the lane effectively impossible
        # to use when the player reached it.
        raft_x = (WIDTH - RAFT_WIDTH) // 2

        self.raft = Raft(
            raft_x,
            RAFT_Y,
            RAFT_WIDTH,
            RAFT_HEIGHT,
            WIDTH,
            2.5
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                self.reset()

        return True

    def update(self):
        if self.game_over or self.won:
            return

        keys = pygame.key.get_pressed()

        # Existing player controls.
        self.player.move(
            keys,
            0,
            WIDTH
        )

        # Move raft continuously.
        self.raft.update()

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        # ---------------------------------------------------------
        # RIVER / RAFT LANE
        # ---------------------------------------------------------
        #
        # Use the player's CENTER to determine whether they have
        # actually entered the raft lane.
        #
        # This prevents losing a life when only the edge of the
        # player's 60px-high collision rectangle touches the river.
        player_center_y = self.player.rect.centery

        player_in_raft_lane = (
            RIVER_TOP
            <= player_center_y
            <= RIVER_BOTTOM
        )

        # Check raft collision using the actual player and raft
        # pygame.Rect objects.
        on_raft = (
            player_in_raft_lane
            and self.player.rect.colliderect(self.raft.rect)
        )

        # If the player is standing on the raft, move them with it.
        if on_raft:
            self.player.rect.x += self.raft.last_dx

            # Keep the player inside the screen.
            self.player.rect.x = max(
                0,
                min(
                    WIDTH - self.player.rect.width,
                    self.player.rect.x
                )
            )

        # If the player has entered the raft lane but is not standing
        # on the raft, lose one life.
        elif player_in_raft_lane and self.hit_cooldown == 0:
            self._lose_life()

            # Stop processing this frame because _lose_life()
            # creates a new player at the starting position.
            return

        # ---------------------------------------------------------
        # TRAFFIC
        # ---------------------------------------------------------

        self.timer += 1

        if self.timer >= self.spawn_interval:
            lane = random.randint(
                0,
                LANES - 1
            )

            self.cars.append(
                make_car(
                    lane,
                    HEIGHT,
                    self.speed
                )
            )

            self.timer = 0

            self.spawn_interval = max(
                22,
                self.spawn_interval - 0.2
            )

        for car in self.cars:
            car.update()

            # Traffic collisions only happen outside the raft lane.
            #
            # The raft lane is handled separately above.
            if (
                self.hit_cooldown == 0
                and not player_in_raft_lane
                and car.rect.colliderect(self.player.rect)
            ):
                self._lose_life()

                # Prevent the same car from immediately hitting
                # the newly respawned player.
                car.rect.y = HEIGHT + 200

                break

        self.cars = [
            car
            for car in self.cars
            if not car.off_screen(HEIGHT)
        ]

        # ---------------------------------------------------------
        # SCORE
        # ---------------------------------------------------------

        self.score += 1

        if self.score % 300 == 0:
            self.speed = min(
                10,
                self.speed + 0.5
            )

        # ---------------------------------------------------------
        # WIN CONDITION
        # ---------------------------------------------------------

        if self.player.rect.top <= 10:
            self.won = True

    def _lose_life(self):
        self.lives -= 1

        # Respawn at the original starting position.
        self.player = Player(
            self.start_x,
            self.start_y
        )

        # Prevent an immediate second collision.
        self.hit_cooldown = 45

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def draw(self):
        self.screen.fill(BG)

        # ---------------------------------------------------------
        # EXISTING ROAD
        # ---------------------------------------------------------

        # Lane markings.
        for i in range(LANES + 1):
            pygame.draw.line(
                self.screen,
                (100, 100, 100),
                (i * LANE_W, 0),
                (i * LANE_W, HEIGHT),
                2
            )

        # Road markings.
        for y in range(0, HEIGHT, 60):
            for i in range(LANES):
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 100),
                    pygame.Rect(
                        i * LANE_W + LANE_W // 2 - 3,
                        y,
                        6,
                        30
                    )
                )

        # Sidewalks.
        pygame.draw.rect(
            self.screen,
            (150, 130, 110),
            pygame.Rect(
                0,
                HEIGHT - 50,
                WIDTH,
                50
            )
        )

        pygame.draw.rect(
            self.screen,
            (150, 130, 110),
            pygame.Rect(
                0,
                0,
                WIDTH,
                30
            )
        )

        # ---------------------------------------------------------
        # TRAFFIC
        # ---------------------------------------------------------

        for car in self.cars:
            car.draw(self.screen)

        # ---------------------------------------------------------
        # RAFT LANE
        # ---------------------------------------------------------

        # Clearly distinguish the raft lane from traffic lanes.
        pygame.draw.rect(
            self.screen,
            (45, 105, 155),
            pygame.Rect(
                0,
                RIVER_TOP,
                WIDTH,
                RIVER_BOTTOM - RIVER_TOP
            )
        )

        # Water details.
        for y in range(
            RIVER_TOP + 12,
            RIVER_BOTTOM,
            24
        ):
            for x in range(0, WIDTH, 36):
                pygame.draw.line(
                    self.screen,
                    (70, 135, 185),
                    (x, y),
                    (x + 16, y),
                    2
                )

        # Moving raft.
        self.raft.draw(self.screen)

        # Player.
        self.player.draw(self.screen)

        # ---------------------------------------------------------
        # HUD
        # ---------------------------------------------------------

        hud = pygame.Rect(
            0,
            0,
            WIDTH,
            30
        )

        pygame.draw.rect(
            self.screen,
            (20, 20, 20),
            hud
        )

        score_text = self.font.render(
            f"Score: {self.score // 10}",
            True,
            (220, 220, 220)
        )

        lives_text = self.font.render(
            f"Lives: {self.lives}",
            True,
            (220, 220, 220)
        )

        goal_text = self.font.render(
            "GOAL: reach the top!",
            True,
            (220, 220, 220)
        )

        restart_text = self.font.render(
            "R=Restart",
            True,
            (220, 220, 220)
        )

        self.screen.blit(
            score_text,
            (6, 4)
        )

        self.screen.blit(
            lives_text,
            (125, 4)
        )

        self.screen.blit(
            goal_text,
            (245, 4)
        )

        self.screen.blit(
            restart_text,
            (500, 4)
        )

        if self.game_over:
            self._msg(
                "CRASHED!",
                (220, 60, 60)
            )

        if self.won:
            self._msg(
                "YOU MADE IT!",
                (80, 220, 80)
            )

        pygame.display.flip()

    def _msg(self, text, color):
        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 150)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        message = self.big_font.render(
            text,
            True,
            color
        )

        sub = self.font.render(
            "Press R to Restart",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            message,
            (
                WIDTH // 2 - message.get_width() // 2,
                HEIGHT // 2 - 40
            )
        )

        self.screen.blit(
            sub,
            (
                WIDTH // 2 - sub.get_width() // 2,
                HEIGHT // 2 + 20
            )
        )

    def run(self):
        running = True

        while running:
            running = self.handle_events()

            self.update()
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()