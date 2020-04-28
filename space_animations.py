import os


def fetch_garbages():
    files_garbages = ['trash_large.txt', 'trash_small.txt', 'trash_xl.txt']
    garbages_frames = []
    for file_garbage in files_garbages:
        path = os.path.join('picture', file_garbage)
        with open(path, 'r') as garbage:
            garbages_frames.append(garbage.read())
    return garbages_frames


def fetch_spaceship_imgs():
    with open('picture/frame1.txt', 'r') as picture:
        frame1 = picture.read()
    with open('picture/frame2.txt', 'r') as picture:
        frame2 = picture.read()
    return frame1, frame2