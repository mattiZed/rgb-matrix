#!/usr/bin/env python3
import sys
import time
from enum import Enum
from itertools import cycle

from PIL import Image, ImageDraw

from rgbmatrix import RGBMatrix, RGBMatrixOptions

MATRIX_ROWS, MATRIX_COLS = 32, 64


options = RGBMatrixOptions()
options.rows = MATRIX_ROWS
options.cols = MATRIX_COLS
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat"

SLEEPRATE = 0.05
ARC = 15

COLORS = cycle([
    (255,   0,   0),
    (127, 127,   0),
    (  0, 255,   0),
    (  0, 127, 127),
    (  0,   0, 255),
    (  127, 0, 127),
])
MATRIX = RGBMatrix(options=options)
BOUNDS = [ (0,0), (31, 31) ]

image = Image.new("RGB", (MATRIX_COLS, MATRIX_ROWS))
draw = ImageDraw.Draw(image)

class ARCStyle(int, Enum):
    sliced = 0
    opening = 1
    closing = 2

def moving_arc(draw: ImageDraw, arc_length: float = 10, style: ARCStyle = ARCStyle.sliced):
    for angle in range(0, 360, arc_length):
        # CLEAR
        draw.rectangle(xy=BOUNDS, fill=(0, 0, 0))

        if style == ARCStyle.sliced:
            start, end = angle, angle + arc_length
        elif style == ARCStyle.opening:
            start, end = angle + arc_length, 360
        elif style == ARCStyle.closing:
            start, end = 0, angle + arc_length

        draw.pieslice(xy=BOUNDS, start=start, end=end, fill=next(COLORS))

        MATRIX.SetImage(image, 16, 0)
        time.sleep(SLEEPRATE)

try:
    while True:
        moving_arc(draw=draw, arc_length=ARC, style=ARCStyle.closing)
        moving_arc(draw=draw, arc_length=ARC, style=ARCStyle.opening)
        moving_arc(draw=draw, arc_length=ARC, style=ARCStyle.sliced)
except KeyboardInterrupt:
    MATRIX.Clear()
    sys.exit(0)
