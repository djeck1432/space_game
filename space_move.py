import asyncio
from itertools import cycle
import space_animations
from physics import update_speed
import curses

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258
BORDER_LINE = 2
SPACESHIP_FRAME = ''
FRAME = ''
OLD_ROW = ''
OLD_COL = ''
FRAME2 = ''

async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)


def draw_frame(canvas, start_row, start_column, text, negative=False):
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def read_controls(canvas, speed=1):
    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction -= speed

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = speed

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = speed

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction -= speed

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def get_frame_size(text):
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns



