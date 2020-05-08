import time
import random
import asyncio
import curses
from itertools import cycle
from tools import read_controls, get_frame_size, draw_frame,fly_garbage,fetch_spaceship_imgs, fetch_garbages,sleep
from physics import update_speed
from obstacles import Obstacle,show_obstacles
from explosion import explode
from game_scenario import get_garbage_delay_tics

obstacles = []
obstacles_in_last_collisions = []
coros = []
GARBAGES = ['duck.txt', 'hubble.txt', 'lamp.txt', 'trash_large.txt', 'trash_small.txt', 'trash_xl.txt']
BORDER_LINE = 2
year = 1957

async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    row, column = start_row, start_column

    global obstacles,obstacles_in_last_collisions

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
        for obstacle in obstacles:
            is_collision = obstacle.has_collision(row, column)
            if is_collision:
                obstacles_in_last_collisions.append(obstacle)
                return None
            else:
                canvas.addstr(round(row), round(column), symbol)
                await asyncio.sleep(0)
                canvas.addstr(round(row), round(column), ' ')
                row += rows_speed
                column += columns_speed

async def show_gameover(canvas):
    window_row_size,window_col_size = canvas.getmaxyx()
    with open('pictures/game_over.txt','r') as text:
        gameover = text.read()
        frame_row_size,frame_col_size = get_frame_size(gameover)
        middle_row = (window_row_size - frame_row_size) // 2
        middle_col = (window_col_size - frame_col_size) // 2
        while True:
            draw_frame(canvas,middle_row,middle_col,gameover)
            await asyncio.sleep(0)


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


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    rows_number, columns_number = canvas.getmaxyx()
    column = max(column, 0)
    column = min(column, columns_number - 1)
    row = 0
    global obstacles,coros
    row_size, col_size = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, row_size, col_size)
    obstacles.append(obstacle)

    while row < rows_number:
        if obstacle in obstacles_in_last_collisions:
            obstacles.remove(obstacle)
            await explode(canvas, row, column)
            return None
        else:
            draw_frame(canvas, row, column, garbage_frame)
            obstacle.row = row
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed


async def create_garbage_coros(canvas):
    window_row_size, window_col_size = canvas.getmaxyx()
    global coros,year
    while True:
        if year < 1961:
            await asyncio.sleep(0)
        else:
            speed = get_garbage_delay_tics(year)
            garbages_frames = fetch_garbages()
            garbage_frame = random.choice(garbages_frames)
            await sleep(random.randint(1, speed))
            coros.append(fly_garbage(canvas, random.randint(2, window_col_size), garbage_frame))


async def animate_spaceship(frame1, frame2):
    frames = cycle([frame1, frame2])
    global FRAME2
    while True:
        for frame in frames:
            global FRAME
            FRAME = frame
            await asyncio.sleep(0)
            FRAME = frame

def control_screen_borders(canvas, row, column):
    window_row_size, window_col_size = canvas.getmaxyx()
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
    return row,column

async def run_spaceship(canvas):
    row_speed = column_speed = 0
    old_frame = ''
    global coros, obstacles,year
    old_row, old_col = row, column = 15, 35
    while True:
        for obstacle in obstacles:
            is_collision = obstacle.has_collision(row, column)
            if is_collision:
                obstacles_in_last_collisions.append(obstacle)
                draw_frame(canvas, row, column, FRAME, negative=True)
                await show_gameover(canvas)
                return None
        else:
            keyboard_row, keyboard_column, space_pressed = read_controls(canvas)
            row_speed, column_speed = update_speed(row_speed,column_speed,keyboard_row,keyboard_column)
            row += row_speed
            column += column_speed
            row,column = control_screen_borders(canvas, row, column)

            if space_pressed and year > 1970:
                coros.append(fire(canvas,row-1,column+2))

            draw_frame(canvas, old_row, old_col, old_frame, negative=True)
            draw_frame(canvas, row, column, FRAME)
            old_frame = FRAME
            old_row, old_col = row, column
            await asyncio.sleep(0)


def create_coros(canvas):
    window_row_size, window_col_size = canvas.getmaxyx()
    frame1, frame2 = fetch_spaceship_imgs()
    star_types = ['+', '*', '.', ':']
    stars_coros = [blink(random.randint(0, 100),
                         canvas,
                         random.randint(BORDER_LINE, window_row_size - BORDER_LINE),
                         random.randint(BORDER_LINE, window_col_size - BORDER_LINE),
                         symbol=random.choice(star_types)
                         ) for _ in range(100)
                   ]
    start_garbage_coro = create_garbage_coros(canvas)
    return [
        animate_spaceship(frame1, frame2),
        *stars_coros,
        run_spaceship(canvas),
        get_year(),
        start_garbage_coro,
    ]


async def get_year():
    global year
    while True:
        year += 1
        await sleep(15)


def draws(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)

    global coros,obstacles,year
    coros = create_coros(canvas)
    while True:
        canvas.border()
        canvas.addstr(40,40,f'Year {year}')
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