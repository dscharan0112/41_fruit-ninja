import pygame
from game.game_engine import GameEngine


pygame.init()

WIDTH, HEIGHT = 700, 600

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slice - Pygame Version")

DARK_BLUE = (20, 25, 45)

clock = pygame.time.Clock()
FPS = 60


def create_engine(difficulty):
    engine = GameEngine(WIDTH, HEIGHT)

    if difficulty == "easy":
        engine.spawn_interval = 70
        engine.bomb_chance = 0.08
        engine.speed_scale = 0.9

    elif difficulty == "medium":
        engine.spawn_interval = 55
        engine.bomb_chance = 0.15
        engine.speed_scale = 1.0

    elif difficulty == "hard":
        engine.spawn_interval = 40
        engine.bomb_chance = 0.25
        engine.speed_scale = 1.1

    return engine


def main():
    engine = create_engine("medium")
    running = True

    while running:
        SCREEN.fill(DARK_BLUE)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif engine.game_over:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1:
                        engine = create_engine("easy")

                    elif event.key == pygame.K_2:
                        engine = create_engine("medium")

                    elif event.key == pygame.K_3:
                        engine = create_engine("hard")

                    elif event.key == pygame.K_ESCAPE:
                        running = False

            else:
                engine.handle_event(event)

        if running:
            engine.handle_input()
            engine.update()
            engine.render(SCREEN)

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()