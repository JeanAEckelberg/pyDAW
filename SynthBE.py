import pygame as py
import numpy as np
import itertools
from scipy import signal as sg
from threading import Thread


class Note:
    sound = 0
    pitch = 0
    name = ''
    type = 0
    sin_tone = 0
    square_tone = 0
    pulse_tone = 0
    saw_tone = 0
    triangle_tone = 0

    def __init__(self, name: str, pitch: float):
        self.pitch = pitch
        self.name = name
        temp = 2 * np.pi * np.arange(44100 * 30) * pitch / 44100
        self.sin_tone = self.sin_tone_gen(temp)
        self.square_tone = self.square_tone_gen(temp)
        self.pulse_tone = self.pulse_tone_gen(temp)
        self.saw_tone = self.saw_tone_gen(temp)
        self.triangle_tone = self.triangle_tone_gen(temp)
        self.sound = self.sin_tone
        self.type = 0

    def play(self):
        self.sound.play(-1)

    def stop(self):
        self.sound.stop()

    def change_wave(self):
        self.type = (self.type + 1) % 5
        match self.type:
            case 0:
                self.sound = self.sin_tone
            case 1:
                self.sound = self.square_tone
            case 2:
                self.sound = self.pulse_tone
            case 3:
                self.sound = self.saw_tone
            case 4:
                self.sound = self.triangle_tone

    def sin_tone_gen(self, pitch: float):
        # rewrite as yield function
        buf = np.cos(pitch).astype(np.float32)
        # buf2 = self.get_sin_oscillator(pitch)
        return py.mixer.Sound(buf)

    def square_tone_gen(self, pitch: float):
        # rewrite as yield function
        buf = sg.square(pitch, duty=0.5).astype(np.float32)
        return py.mixer.Sound(buf)

    def pulse_tone_gen(self, pitch: float):
        # rewrite as yield function
        buf = sg.square(pitch, duty=0.25).astype(np.float32)
        return py.mixer.Sound(buf)

    def saw_tone_gen(self, pitch: float):
        # rewrite as yield function
        buf = sg.sawtooth(pitch).astype(np.float32)
        return py.mixer.Sound(buf)

    def triangle_tone_gen(self, pitch: float):
        # rewrite as yield function
        buf = sg.sawtooth(pitch, width=0.5).astype(np.float32)
        return py.mixer.Sound(buf)


    def get_sin_oscillator(self, freq, amp=1, phase=0, sample_rate=44100):

        phase = (phase / 360) * 2 * np.pi

        increment = (2 * np.pi * freq) / sample_rate

        return (np.sin(phase + v) * amp for v in itertools.count(start=0, step=increment))
