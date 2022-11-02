import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1
        self.randomize = randomize

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        return [[random.randint(0, 1) if randomize else 0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        res = []
        shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for shift in shifts:
            cur_neigh_inxs = cell[0] + shift[0], cell[1] + shift[1]
            if 0 <= cur_neigh_inxs[0] < self.rows and 0 <= cur_neigh_inxs[1] < self.cols:
                res.append(self.curr_generation[cur_neigh_inxs[0]][cur_neigh_inxs[1]])
        return res

    def get_next_generation(self) -> Grid:
        next_gen_grid = self.create_grid(False)
        for i in range(self.rows):
            for j in range(self.cols):
                cur_cell_neigh = self.get_neighbours((i, j))
                n_count = sum(cur_cell_neigh)
                if (self.curr_generation[i][j] and 2 <= n_count <= 3) or ((not self.curr_generation[i][j]) and n_count == 3):
                    next_gen_grid[i][j] = 1
        return next_gen_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        n_g = self.get_next_generation()
        self.prev_generation = self.curr_generation
        self.curr_generation = n_g
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations == self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            data = f.readlines()
            game = GameOfLife((len(data) - 1, len(data[0]) - 1))
            game.curr_generation = [[int(data[i][j]) for j in range(len(data[i].strip()))] for i in range(len(data) - 1)]
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for i in range(self.rows):
                print("".join(list(map(str, self.curr_generation[i]))), file=f)


if __name__ == "__main__":
    ng = GameOfLife.from_file(pathlib.Path('C:\\Users\\Nikita\\PycharmProjects\\nikita-itmo-gh-acc\\homework03\\glider.txt'))
    ng.save(pathlib.Path("C:\\Users\\Nikita\\PycharmProjects\\nikita-itmo-gh-acc\\homework03\\test_save1.txt"))
