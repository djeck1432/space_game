import asyncio
import os

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


def read_controls(canvas):

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed



def get_frame_size(text):
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns

def fetch_garbages():
    files_garbages = ['trash_large.txt', 'trash_small.txt', 'trash_xl.txt']
    garbages_frames = []
    for file_garbage in files_garbages:
        path = os.path.join('pictures', file_garbage)
        with open(path, 'r') as garbage:
            garbages_frames.append(garbage.read())
    return garbages_frames


def fetch_spaceship_imgs():
    with open('pictures/frame1.txt', 'r') as picture:
        frame1 = picture.read()
    with open('pictures/frame2.txt', 'r') as picture:
        frame2 = picture.read()
    return frame1, frame2



