import asyncio
import curses
import random
import time
from space_animations import fetch_spaceship_imgs

BORDER_LINE = 2


async def blink(random_ignition, canvas, row, column, symbol='*'):
    for _ in range(random_ignition):
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(20)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(5)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(3)


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
    return stars_coros


async def sleep(tics=1):
    await asyncio.sleep(tics)




def draws(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)
    frame1, frame2 = fetch_spaceship_imgs()
    coros = create_coros(canvas, frame1, frame2)
    while True:
        asyncio.run(coros)
        # for coro in coros.copy():
        #     try:
        #         coro.send(None)
        #     except StopIteration:
        #         coros.remove(coro)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draws)