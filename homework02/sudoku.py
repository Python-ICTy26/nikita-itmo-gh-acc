import copy
import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    result = list()
    length = len(values)
    part = length // n
    for i in range(n):
        start = part * i
        result.append(values[start : start + part])
    return result


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [elem[pos[1]] for elem in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row_min = pos[0] - pos[0] % 3
    col_min = pos[1] - pos[1] % 3
    return [grid[row_min + i][col_min + j] for i in range(3) for j in range(3)]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    n = len(grid)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == ".":
                return i, j
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    base = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
    cur: tp.Set[str] = set()
    all_ = get_row(grid, pos), get_col(grid, pos), get_block(grid, pos)
    for param in all_:
        cur = cur.union(set([el for el in param if el != "."]))
    return base.difference(cur)


solved = False
depth = 0


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    global solved, depth
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    if depth == 0:
        solved = False
    pos = find_empty_positions(grid)
    if pos:
        p_values = find_possible_values(grid, pos)
        for item in p_values:
            grid[pos[0]][pos[1]] = item
            depth += 1
            solve(grid)
            depth -= 1
            if solved:
                return grid
            grid[pos[0]][pos[1]] = "."
    else:
        solved = True
    return grid


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles
    n = len(solution)
    for i in range(n):
        for j in range(n):
            row, col, block = (
                get_row(solution, (i, j)),
                get_col(solution, (i, j)),
                get_block(solution, (i, j)),
            )
            if (
                solution[i][j] == "."
                or len(row) != len(set(row))
                or len(col) != len(set(col))
                or len(block) != len(set(block))
            ):
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    # """Генерация судоку заполненного на N элементов
    #
    # >>> grid = generate_sudoku(40)
    # >>> sum(1 for row in grid for e in row if e == '.')
    # 41
    # >>> solution = solve(grid)
    # >>> check_solution(solution)
    # True
    # >>> grid = generate_sudoku(1000)
    # >>> sum(1 for row in grid for e in row if e == '.')
    # 0
    # >>> solution = solve(grid)
    # >>> check_solution(solution)
    # True
    # >>> grid = generate_sudoku(0)
    # >>> sum(1 for row in grid for e in row if e == '.')
    # 81
    # >>> solution = solve(grid)
    # >>> check_solution(solution)
    # True
    # """
    if N > 81:
        N = 81
    n = 9
    template: tp.List[tp.List[str]] = [["." for _ in range(n)] for _ in range(n)]
    index_pairs = [(x, y) for x in range(n) for y in range(n)]
    base: tp.List[str] = [str(k) for k in range(1, n + 1)]
    for i in range(n):
        j = random.randint(0, n - 1)
        template[i][j] = base.pop(random.randint(0, len(base) - 1))
    template_: tp.Optional[tp.List[tp.List[str]]] = solve(template)
    if template_ is not None:
        for _ in range(n * n - N):
            i, j = index_pairs.pop(random.randint(0, len(index_pairs) - 1))
            template_[i][j] = "."
        template = template_
    return template


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
