# This is a sample Python script.
import time

import pygame as py
import sys
import SynthBE as sbe
import numpy as np
import pitch_data
from pitch_data import pitches

size = width, height = 1920, 1080
black = 0, 0, 0
screen = py.display.set_mode(size)
clock = py.time.Clock()
offset = 3


py.mixer.pre_init(size=32, frequency=44100)
py.init()

simple_font = py.font.SysFont('malgungothic', 50)

def switch(key):
    key_tester = {
        py.K_a: 1,
        py.K_w: 2,
        py.K_s: 3,
        py.K_e: 4,
        py.K_d: 5,
        py.K_f: 6,
        py.K_t: 7,
        py.K_g: 8,
        py.K_y: 9,
        py.K_h: 10,
        py.K_u: 11,
        py.K_j: 12,
        py.K_k: 13,
        py.K_o: 14,
        py.K_l: 15
    }
    return key_tester.get(key, -1)


def create_notes():
    init_time = time.time()
    notes = [0] * len(pitch_data.pitches.values())

    title = simple_font.render('pyDAW', False, (255, 255, 255))
    title_rect = title.get_rect()
    title_rect.center = screen.get_rect().center[0], screen.get_rect().center[1] - 100
    # slow as fuck
    for i, name_pitch in enumerate(pitch_data.pitches.items()):
        notes[i] = sbe.Note(name_pitch[0], name_pitch[1])

        screen.blit(title, title_rect)
        py.draw.rect(screen, (255, 255, 255), py.Rect(710, 520, 500 * i/ len(pitch_data.pitches.keys()), 40))
        py.draw.rect(screen, (128, 128, 128), py.Rect(710, 520, 500, 40), 5)
        py.display.flip()

    end_time = time.time()
    print(end_time - init_time)
    return notes


def load():
    init_time = time.time()

    py.mixer.init()
    noteList = create_notes()
    end_time = time.time()
    print(end_time - init_time)
    return noteList


def loop(noteList, offset):
    while 1:
        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE: sys.exit()
                if switch(event.key) != -1 and offset * 12 + switch(event.key) < len(noteList):
                    noteList[offset * 12 + switch(event.key)].play()
                # [x.play() for x in noteList if x.pitch == switch(event.key)]
                # map(lambda x: x.play(), list(filter(lambda x: x.pitch == switch(event.key), noteList)))

            if event.type == py.KEYUP:
                if event.key == py.K_z:
                    offset -= 1 if offset > 0 else 0
                if event.key == py.K_x:
                    offset += 1 if offset < 8 else 0
                if event.key == py.K_c:
                    init_time = time.time()
                    [x.change_wave() for x in noteList]
                    end_time = time.time()
                    print(end_time - init_time)
                if switch(event.key) != -1 and offset * 12 + switch(event.key) < len(noteList):
                    noteList[offset * 12 + switch(event.key)].stop()
                # [x.stop() for x in noteList if x.pitch == switch(event.key)]
                # map(lambda x: x.stop(), list(filter(lambda x: x.pitch == switch(event.key), noteList)))

        # DO ACTIONS
        # screen.fill((0, 0, 0))
        screen.fill((255, 255, 255))

        # screen.blit(title, titlerect)

        # Render Frame
        py.display.flip()

        clock.tick(60)


def close():
    return 0


# Press the green button to run the script.
if __name__ == '__main__':
    noteList = load()
    # screen.fill((255, 255, 255))
    # py.display.flip()
    loop(noteList, 3)
    close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
