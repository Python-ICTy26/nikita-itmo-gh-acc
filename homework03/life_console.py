import argparse
import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen_y, screen_x = screen.getmaxyx()
        b_line = "+" + self.life.cols * "-" + "+"
        screen.addstr(0, 0, b_line)
        screen.addstr(self.life.rows + 1, 0, b_line)
        for y in range(self.life.rows):
            screen.addch(y + 1, 0, "|")
            screen.addch(y + 1, self.life.cols + 1, "|")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for y in range(0, self.life.rows):
            for x in range(0, self.life.cols):
                if self.life.curr_generation[y][x]:
                    try:
                        screen.addch(y + 1, x + 1, ord("*"))
                    except curses.error:
                        pass

    def run(self) -> None:
        screen = curses.initscr()
        curses.resize_term(self.life.rows + 100, self.life.cols + 100)
        #screen.resize(self.life.rows + 2, self.life.cols + 2)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            screen.clear()
            self.life.step()
            self.draw_grid(screen)
            self.draw_borders(screen)
            screen.refresh()
        curses.endwin()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--cols", type=int, default=48)
    parser.add_argument("--rows", type=int, default=32)
    parser.add_argument("--max_generations", type=int, default=256)
    args = parser.parse_args()
    lf = GameOfLife((args.rows, args.cols), max_generations=args.max_generations)
    ui = Console(lf)
    ui.run()
