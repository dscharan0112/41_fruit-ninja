import pygame
import random
import math
import os

from .fruit import Fruit


WHITE = (255, 255, 255)
BOMB_BLACK = (30, 30, 30)

FRUIT_COLORS = [
    (220, 60, 60),
    (230, 140, 40),
    (230, 200, 40),
    (90, 180, 90)
]


class GameEngine:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.fruits = []

        self.trail = []
        self.last_mouse_pos = None

        self.spawn_interval = 55
        self._spawn_timer = 0

        self.bomb_chance = 0.15
        self.speed_scale = 1.0

        self.lives = 3
        self.score = 0

        self.font = pygame.font.SysFont("Arial", 28)

        self.game_over_font = pygame.font.SysFont(
            "Arial",
            64
        )

        self.final_score_font = pygame.font.SysFont(
            "Arial",
            36
        )

        self.replay_font = pygame.font.SysFont(
            "Arial",
            28
        )

        self.game_over = False

        self.game_over_sound_played = False

        # Find the project root folder
        project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        sound_folder = os.path.join(
            project_root,
            "sounds"
        )

        # Load sound effects
        self.slice_sound = pygame.mixer.Sound(
            os.path.join(
                sound_folder,
                "slice.wav"
            )
        )

        self.bomb_sound = pygame.mixer.Sound(
            os.path.join(
                sound_folder,
                "bomb.wav"
            )
        )

        self.game_over_sound = pygame.mixer.Sound(
            os.path.join(
                sound_folder,
                "game_over.wav"
            )
        )

    def spawn_fruit(self):

        x = random.randint(
            60,
            self.width - 60
        )

        vy = -random.uniform(
            13,
            16
        ) * self.speed_scale

        vx = random.uniform(
            -2,
            2
        )

        gravity = 0.35

        kind = (
            "bomb"
            if random.random() < self.bomb_chance
            else "fruit"
        )

        fruit = Fruit(
            x,
            self.height + 30,
            vx,
            vy,
            gravity,
            kind=kind
        )

        fruit.color = (
            BOMB_BLACK
            if kind == "bomb"
            else random.choice(FRUIT_COLORS)
        )

        self.fruits.append(fruit)

    def handle_event(self, event):

        if event.type == pygame.MOUSEMOTION:
            self._handle_motion(event.pos)

    def _handle_motion(self, pos):

        if self.last_mouse_pos is not None:

            x1, y1 = self.last_mouse_pos
            x2, y2 = pos

            for fruit in self.fruits:

                if fruit.sliced:
                    continue

                cx = fruit.x
                cy = fruit.y

                dx = x2 - x1
                dy = y2 - y1

                if dx == 0 and dy == 0:

                    distance = math.hypot(
                        cx - x2,
                        cy - y2
                    )

                else:

                    t = (
                        (cx - x1) * dx
                        + (cy - y1) * dy
                    ) / (
                        dx * dx
                        + dy * dy
                    )

                    t = max(
                        0,
                        min(1, t)
                    )

                    closest_x = x1 + t * dx
                    closest_y = y1 + t * dy

                    distance = math.hypot(
                        cx - closest_x,
                        cy - closest_y
                    )

                if distance <= fruit.radius:
                    self._slice(fruit)

        self.last_mouse_pos = pos

        self.trail.append(pos)

        if len(self.trail) > 15:
            self.trail.pop(0)

    def _slice(self, fruit):

        fruit.sliced = True

        if fruit.kind == "bomb":

            self.bomb_sound.play()

            self.game_over = True

        else:

            self.score += 1

            self.slice_sound.play()

    def handle_input(self):

        pass

    def update(self):

        if self.game_over:
            return

        self._spawn_timer += 1

        if self._spawn_timer >= self.spawn_interval:

            self._spawn_timer = 0

            self.spawn_fruit()

        still_alive = []

        for fruit in self.fruits:

            fruit.update()

            if fruit.sliced:
                continue

            if fruit.off_screen(self.height):

                if fruit.kind == "fruit":

                    self.lives -= 1

                continue

            still_alive.append(fruit)

        self.fruits = still_alive

        if self.lives <= 0:

            self.game_over = True

    def render(self, screen):

        # Draw fruits
        for fruit in self.fruits:

            color = getattr(
                fruit,
                "color",
                WHITE
            )

            pygame.draw.circle(
                screen,
                color,
                (
                    int(fruit.x),
                    int(fruit.y)
                ),
                fruit.radius
            )

        # Draw mouse trail
        if len(self.trail) >= 2:

            pygame.draw.lines(
                screen,
                WHITE,
                False,
                self.trail,
                3
            )

        # Score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        # Lives
        lives_text = self.font.render(
            f"Lives: {self.lives}",
            True,
            WHITE
        )

        screen.blit(
            lives_text,
            (
                self.width - 130,
                10
            )
        )

        # Game Over screen
        if self.game_over:

            # Play game-over sound only once
            if not self.game_over_sound_played:

                self.game_over_sound.play()

                self.game_over_sound_played = True

            # Dark overlay
            overlay = pygame.Surface(
                (
                    self.width,
                    self.height
                ),
                pygame.SRCALPHA
            )

            overlay.fill(
                (
                    0,
                    0,
                    0,
                    180
                )
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            # GAME OVER
            game_over_text = self.game_over_font.render(
                "GAME OVER",
                True,
                (255, 80, 80)
            )

            screen.blit(
                game_over_text,
                game_over_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 100
                    )
                )
            )

            # Final Score
            final_score_text = self.final_score_font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            screen.blit(
                final_score_text,
                final_score_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 30
                    )
                )
            )

            # Difficulty options
            replay_text = self.replay_font.render(
                "1 - EASY    2 - MEDIUM    3 - HARD",
                True,
                WHITE
            )

            screen.blit(
                replay_text,
                replay_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 30
                    )
                )
            )

            # Exit
            exit_text = self.replay_font.render(
                "ESC - EXIT",
                True,
                WHITE
            )

            screen.blit(
                exit_text,
                exit_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 75
                    )
                )
            )