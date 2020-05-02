import time
import random
import asyncio
import web_pdb
import curses
from itertools import cycle
from space_move import BORDER_LINE, sleep
from space_animations import fetch_spaceship_imgs, fetch_garbages
from space_garbage import fly_garbage
from space_move import read_controls, get_frame_size, draw_frame
from physics import update_speed

coros = []
GARBAGES = ['duck.txt', 'hubble.txt', 'lamp.txt', 'trash_large.txt', 'trash_small.txt', 'trash_xl.txt']


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(random_ignition, canvas, row, column, symbol='*'):
    for _ in range(random_ignition):
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)
    while True:
        await sleep(20)
        canvas.addstr(row, column, symbol, curses.A_DIM)

        await sleep(3)
        canvas.addstr(row, column, symbol)

        await sleep(5)
        canvas.addstr(row, column, symbol, curses.A_BOLD)

        await sleep(3)
        canvas.addstr(row, column, symbol)


async def create_garbage_coros(canvas):
    row, col = canvas.getmaxyx()
    global coros
    while True:
        garbages_frames = fetch_garbages()
        garbage_frame = random.choice(garbages_frames)
        await sleep(random.randint(1, 12))
        coros.append(fly_garbage(canvas, random.randint(2, col), garbage_frame))


async def animate_spaceship(frame1, frame2):
    frames = cycle([frame1, frame2])
    global FRAME2
    while True:
        for frame in frames:
            global FRAME
            FRAME = frame
            await asyncio.sleep(0)
            FRAME = frame



async def run_spaceships(canvas):
    window_row_size, window_col_size = canvas.getmaxyx()
    row, column = 15, 35
    row_speed = column_speed = 0
    old_frame = ''
    global OLD_ROW, OLD_COL, FRAME2, coros
    OLD_ROW, OLD_COL = row, column
    _, frame2 = fetch_spaceship_imgs()
    while True:
        keyboard_row, keyboard_column, space_pressed = read_controls(canvas)
        row_speed, column_speed = update_speed(row_speed,column_speed,keyboard_row,keyboard_column)
        row += row_speed
        column += column_speed
        frame_row, frame_column = get_frame_size(FRAME)
        border_col = window_col_size - frame_column
        border_row = window_row_size - frame_row

        if row <= 0:
            row = 1
        elif border_row <= row:
            row = window_row_size - (frame_row + BORDER_LINE)
        elif column <= 0:
            column = 2
        elif border_col <= column:
            column = window_col_size - (frame_column + BORDER_LINE)
        else:
            row, column

        if space_pressed:
            coros.append(fire(canvas,row-1,column+2))

        draw_frame(canvas, OLD_ROW, OLD_COL, old_frame, negative=True)
        draw_frame(canvas, row, column, FRAME)
        old_frame = FRAME
        OLD_ROW, OLD_COL = row, column
        await asyncio.sleep(0)

        draw_frame(canvas, OLD_ROW, OLD_COL, old_frame, negative=True)
        draw_frame(canvas, row, column, FRAME)
        old_frame = FRAME
        OLD_ROW, OLD_COL = row, column

def create_coros(canvas, frame1, frame2):
    window_size_row, window_size_col = canvas.getmaxyx()
    start_types = ['+', '*', '.', ':']
    stars_coros = [blink(random.randint(0, 100),
                         canvas,
                         random.randint(BORDER_LINE, window_size_row - BORDER_LINE),
                         random.randint(BORDER_LINE, window_size_col - BORDER_LINE),
                         symbol=random.choice(start_types)
                         ) for _ in range(100)
                   ]

    return [
        animate_spaceship(frame1, frame2),
        *stars_coros,
        run_spaceships(canvas),
    ]


def draws(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)

    frame1, frame2 = fetch_spaceship_imgs()
    start_garbage_coro = create_garbage_coros(canvas)
    global coros
    coros = create_coros(canvas, frame1, frame2)
    while True:
        #start_garbage_coro.send(None)
        for coro in coros.copy():
            try:
                coro.send(None)
            except StopIteration:
                coros.remove(coro)

        time.sleep(0.1)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draws)