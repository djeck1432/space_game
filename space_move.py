import asyncio
from itertools import cycle
from physics import update_speed

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258
BORDER_LINE = 2
SPACESHIP_FRAME = ''
FRAME = ''

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

# def read_controls(canvas, speed=10):
#     rows_direction = columns_direction = 0
#     space_pressed = False
#
#     while True:
#         pressed_key_code = canvas.getch()
#
#         if pressed_key_code == -1:
#             break
#
#         if pressed_key_code == UP_KEY_CODE:
#             rows_direction -= speed
#
#         if pressed_key_code == DOWN_KEY_CODE:
#             rows_direction = speed
#
#         if pressed_key_code == RIGHT_KEY_CODE:
#             columns_direction = speed
#
#         if pressed_key_code == LEFT_KEY_CODE:
#             columns_direction -= speed
#
#         if pressed_key_code == SPACE_KEY_CODE:
#             space_pressed = True
#
#     return rows_direction, columns_direction, space_pressed


async def animate_spaceship(canvas, frame1, frame2):
    row, column = 4, 6
    frames = cycle([frame1, frame2])
    for frame in frames:
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        old_row = row
        old_column = column
        row, column = get_coordinates(canvas, row, column, frame)
        draw_frame(canvas, old_row, old_column, frame, negative=True)


# def get_control_speed(canvas):
#     row_speed = column_speed = 0
#     keyboard_row, keyboard_column, space_pressed = read_controls(canvas)
#     row_speed, column_speed = update_speed(row_speed, column_speed, keyboard_row, keyboard_column)
#     return row_speed, column_speed


def get_coordinates(canvas, row, column, frame1,frame2):
    window_row_size, window_col_size = canvas.getmaxyx()
    keyboard_row, keyboard_column, space_pressed = read_controls(canvas)
    row, column = 4, 6
    # keyboard_row, keyboard_column = get_control_speed(canvas)
    row += keyboard_row
    column += keyboard_column
    frame_row, frame_column = get_frame_size(frame1)
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

    frames = cycle([frame1, frame2])
    for frame in frames:
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        old_row = row
        old_column = column
        row, column = get_coordinates(canvas, row, column, frame)
        draw_frame(canvas, old_row, old_column, frame, negative=True)
    # return row, column


# def get_coordinates(canvas, row, column, frame1):
#     window_row_size, window_col_size = canvas.getmaxyx()
#     keyboard_row, keyboard_column, space_pressed = read_controls(canvas)
#     row += keyboard_row
#     column += keyboard_column
#     frame_row, frame_column = get_frame_size(frame1)
#     border_col = window_col_size - frame_column
#     border_row = window_row_size - frame_row
#
#     if row <= 0:
#         row = 1
#     elif border_row <= row:
#         row = window_row_size - (frame_row + BORDER_LINE)
#     elif column <= 0:
#         column = 2
#     elif border_col <= column:
#         column = window_col_size - (frame_column + BORDER_LINE)
#     else:
#         row, column
#     return row, column


def get_frame_size(text):
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns
