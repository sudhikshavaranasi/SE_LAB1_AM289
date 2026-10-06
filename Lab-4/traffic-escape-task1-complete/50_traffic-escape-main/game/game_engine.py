import pygame
import random
import json
import os

from game.player import Player, LANE_W
from game.traffic import Car, make_car
from game.raft import Raft


LANES = 8
WIDTH = LANES * LANE_W
HEIGHT = 600
FPS = 60

BG = (60, 60, 60)

RIVER_TOP = 255
RIVER_BOTTOM = 345
RAFT_Y = RIVER_TOP + 8
RAFT_WIDTH = 260

MAX_HIGH_SCORES = 5

# Store the score file in the project root.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCORES_FILE = os.path.join(PROJECT_ROOT, "scores.json")


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

        self.high_scores = self.load_scores()

        self.reset()

    # ============================================================
    # HIGH SCORE SYSTEM
    # ============================================================

    def load_scores(self):
        """
        Load high scores from scores.json.

        If the file does not exist, create it automatically with
        an empty score list.
        """
        if not os.path.exists(SCORES_FILE):
            try:
                with open(SCORES_FILE, "w", encoding="utf-8") as file:
                    json.dump([], file, indent=4)
            except OSError:
                pass

            return []

        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                return []

            scores = []

            for score in data:
                if isinstance(score, (int, float)):
                    scores.append(int(score))

            scores.sort(reverse=True)

            return scores[:MAX_HIGH_SCORES]

        except (json.JSONDecodeError, OSError):
            return []

    def save_score(self):
        """
        Add the current score to the high score table, sort it from
        highest to lowest, keep only the top five, and save it.
        """
        score = self.score // 10

        self.high_scores.append(score)

        self.high_scores.sort(reverse=True)

        self.high_scores = self.high_scores[:MAX_HIGH_SCORES]

        try:
            with open(SCORES_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    self.high_scores,
                    file,
                    indent=4
                )
        except OSError:
            pass

        self.score_saved = True

    # ============================================================
    # RESET / GAME STATE
    # ============================================================

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

        # Existing scoring system.
        self.score = 0

        # Existing 3-lives system.
        self.lives = 3

        self.game_over = False
        self.won = False

        self.hit_cooldown = 0

        # Prevent the same game from being saved multiple times.
        self.score_saved = False

        self.raft = Raft(
            RAFT_Y,
            RAFT_WIDTH,
            WIDTH,
            2.5
        )

    # ============================================================
    # EVENTS
    # ============================================================

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

    # ============================================================
    # GAME UPDATE
    # ============================================================

    def update(self):
        if self.game_over or self.won:
            return

        keys = pygame.key.get_pressed()

        # Existing player movement.
        self.player.move(
            keys,
            0,
            WIDTH
        )

        # Existing moving raft.
        self.raft.update()

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        # --------------------------------------------------------
        # RAFT LANE
        # --------------------------------------------------------

        player_in_river = (
            RIVER_TOP
            <= self.player.rect.centery
            <= RIVER_BOTTOM
        )

        # --------------------------------------------------------
        # TRAFFIC SPAWNING
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # TRAFFIC MOVEMENT / COLLISION
        # --------------------------------------------------------

        for car in self.cars:

            car.update()

            if (
                self.hit_cooldown == 0
                and not player_in_river
                and car.rect.colliderect(
                    self.player.rect
                )
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

        # --------------------------------------------------------
        # RAFT COLLISION / CARRYING
        # --------------------------------------------------------

        if (
            player_in_river
            and self.hit_cooldown == 0
        ):
            on_raft = self.player.rect.colliderect(
                self.raft.rect
            )

            if on_raft:
                # Carry the player horizontally with the raft.
                self.player.rect.x += round(
                    self.raft.speed
                )

                # Keep player inside the screen.
                self.player.rect.x = max(
                    0,
                    min(
                        WIDTH - self.player.rect.width,
                        self.player.rect.x
                    )
                )

            else:
                # Player is in the river but not on the raft.
                self._lose_life()

                return

        # --------------------------------------------------------
        # EXISTING SCORING
        # --------------------------------------------------------

        self.score += 1

        if self.score % 300 == 0:
            self.speed = min(
                10,
                self.speed + 0.5
            )

        # --------------------------------------------------------
        # EXISTING WIN CONDITION
        # --------------------------------------------------------

        if self.player.rect.top <= 10:
            self.won = True

            if not self.score_saved:
                self.save_score()

    # ============================================================
    # LIVES
    # ============================================================

    def _lose_life(self):
        self.lives -= 1

        self.player = Player(
            self.start_x,
            self.start_y
        )

        self.hit_cooldown = 45

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

            if not self.score_saved:
                self.save_score()

    # ============================================================
    # DRAW
    # ============================================================

    def draw(self):
        self.screen.fill(BG)

        # --------------------------------------------------------
        # ROAD MARKINGS
        # --------------------------------------------------------

        for i in range(LANES + 1):
            pygame.draw.line(
                self.screen,
                (100, 100, 100),
                (i * LANE_W, 0),
                (i * LANE_W, HEIGHT),
                2
            )

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

        # --------------------------------------------------------
        # SIDEWALKS
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # TRAFFIC
        # --------------------------------------------------------

        for car in self.cars:
            car.draw(self.screen)

        # --------------------------------------------------------
        # RIVER / RAFT LANE
        # --------------------------------------------------------

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

        for y in range(
            RIVER_TOP + 12,
            RIVER_BOTTOM,
            24
        ):
            for x in range(
                0,
                WIDTH,
                36
            ):
                pygame.draw.line(
                    self.screen,
                    (70, 135, 185),
                    (x, y),
                    (x + 16, y),
                    2
                )

        self.raft.draw(
            self.screen
        )

        # --------------------------------------------------------
        # PLAYER
        # --------------------------------------------------------

        self.player.draw(
            self.screen
        )

        # --------------------------------------------------------
        # HUD
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # GAME OVER / WIN
        # --------------------------------------------------------

        if self.game_over:
            self._draw_game_over()

        elif self.won:
            self._draw_win()

        pygame.display.flip()

    # ============================================================
    # GAME OVER SCREEN
    # ============================================================

    def _draw_game_over(self):
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
            "CRASHED!",
            True,
            (220, 60, 60)
        )

        score_message = self.font.render(
            f"Score: {self.score // 10}",
            True,
            (240, 240, 240)
        )

        self.screen.blit(
            message,
            (
                WIDTH // 2 - message.get_width() // 2,
                HEIGHT // 2 - 100
            )
        )

        self.screen.blit(
            score_message,
            (
                WIDTH // 2 - score_message.get_width() // 2,
                HEIGHT // 2 - 45
            )
        )

        self._draw_high_scores(
            HEIGHT // 2
        )

        restart = self.font.render(
            "Press R to Restart",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            restart,
            (
                WIDTH // 2 - restart.get_width() // 2,
                HEIGHT - 45
            )
        )

    # ============================================================
    # WIN SCREEN
    # ============================================================

    def _draw_win(self):
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
            "YOU MADE IT!",
            True,
            (80, 220, 80)
        )

        score_message = self.font.render(
            f"Score: {self.score // 10}",
            True,
            (240, 240, 240)
        )

        self.screen.blit(
            message,
            (
                WIDTH // 2 - message.get_width() // 2,
                HEIGHT // 2 - 100
            )
        )

        self.screen.blit(
            score_message,
            (
                WIDTH // 2 - score_message.get_width() // 2,
                HEIGHT // 2 - 45
            )
        )

        self._draw_high_scores(
            HEIGHT // 2
        )

        restart = self.font.render(
            "Press R to Restart",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            restart,
            (
                WIDTH // 2 - restart.get_width() // 2,
                HEIGHT - 45
            )
        )

    # ============================================================
    # HIGH SCORE DISPLAY
    # ============================================================

    def _draw_high_scores(self, start_y):
        title = self.font.render(
            "TOP 5 SCORES",
            True,
            (255, 220, 80)
        )

        self.screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                start_y
            )
        )

        if not self.high_scores:
            empty = self.font.render(
                "No scores yet",
                True,
                (200, 200, 200)
            )

            self.screen.blit(
                empty,
                (
                    WIDTH // 2 - empty.get_width() // 2,
                    start_y + 30
                )
            )

            return

        for index, score in enumerate(
            self.high_scores[:MAX_HIGH_SCORES]
        ):
            score_text = self.font.render(
                f"{index + 1}. {score}",
                True,
                (240, 240, 240)
            )

            self.screen.blit(
                score_text,
                (
                    WIDTH // 2 - score_text.get_width() // 2,
                    start_y + 30 + index * 25
                )
            )

    # ============================================================
    # MAIN LOOP
    # ============================================================

    def run(self):
        running = True

        while running:
            running = self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()