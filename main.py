from curses import wrapper, window
import curses
from queue import Queue
import time

maze: list[list[str]] = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", "#", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"],
]


def print_maze(stdscr: window, path: list[tuple[int, int]] = []) -> None:
    GREEN = curses.color_pair(1)
    MAGENTA = curses.color_pair(2)

    for i, rows in enumerate(maze):
        for j, char in enumerate(rows):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "@", MAGENTA)
            else:
                stdscr.addstr(i, j * 2, char, GREEN)


def find_start_char_position(start_char: str) -> tuple[int, int] | None:
    for row, rows in enumerate(maze):
        for col, char in enumerate(rows):
            if char == start_char:
                return (row, col)

    return None


def find_path(stdscr: window) -> list[tuple[int, int]] | None:
    start_ch = "O"
    end_ch = "X"

    start_pos = find_start_char_position(start_ch)

    if start_pos is None:
        raise ValueError(f"Start character {start_ch} not found in maze")

    q: Queue[list[tuple[int, int]]] = Queue()
    q.put([start_pos])

    visited: set[tuple[int, int]] = set()

    while not q.empty():
        path = q.get()
        (row, col) = path[-1]

        stdscr.clear()
        print_maze(stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end_ch:
            return path

        neighbors = find_neighbors(row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor

            if maze[r][c] == "#":
                continue

            q.put(path + [neighbor])
            visited.add(neighbor)

    return None


def find_neighbors(row: int, col: int) -> list[tuple[int, int]]:
    neighbors = []

    if row > 0:
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr: window) -> None:
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    stdscr.clear()
    find_path(stdscr)
    stdscr.refresh()
    stdscr.getch()


wrapper(main)
