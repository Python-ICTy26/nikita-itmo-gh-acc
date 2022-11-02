import argparse
import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen_size = self.life.cols * self.cell_size, self.life.rows * self.cell_size
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self, screen) -> None:
        for x in range(0, self.screen_size[0], self.cell_size):
            pygame.draw.line(screen, pygame.Color("black"), (x, 0), (x, self.screen_size[1]))
        for y in range(0, self.screen_size[1], self.cell_size):
            pygame.draw.line(screen, pygame.Color("black"), (0, y), (self.screen_size[0], y))

    def draw_grid(self, screen) -> None:
        for y in range(0, self.screen_size[1], self.cell_size):
            for x in range(0, self.screen_size[0], self.cell_size):
                pygame.draw.rect(screen, pygame.Color((255, 255, 255)),
                                 (x, y, x + self.cell_size, y + self.cell_size))
                if self.life.curr_generation[y // self.cell_size][x // self.cell_size]:
                    pygame.draw.rect(screen, pygame.Color((0, 255, 0)),
                                     (x, y, x + self.cell_size, y + self.cell_size))
        return None

    def set_configuration(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_s]:
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos[0] // self.cell_size, event.pos[1] // self.cell_size
                    if event.button == 1:
                        self.life.curr_generation[y][x] = 1
                    elif event.button == 3:
                        self.life.curr_generation[y][x] = 0
            self.draw_grid(self.screen)
            self.draw_lines(self.screen)
            pygame.display.flip()

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        if not self.life.randomize:
            self.set_configuration()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        quit_, pause = False, False
        while self.life.is_changing and not self.life.is_max_generations_exceeded and not quit_:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit_ = True
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_p]:
                        pause = not pause
            if not pause:
                self.life.step()
                self.draw_grid(self.screen)
                self.draw_lines(self.screen)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--width", type=int, default=48)
    parser.add_argument("--height", type=int, default=32)
    parser.add_argument("--cell_size", type=int, default=16)
    args = parser.parse_args()
    gm = GUI(GameOfLife((args.height, args.width), True, 200), cell_size=args.cell_size)
    #gm = GUI(GameOfLife((30, 40), True, 200), cell_size=20)
    gm.run()
