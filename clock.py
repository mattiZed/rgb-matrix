import sys
import time
from calendar import monthrange
from datetime import datetime, timedelta, timezone

from PIL import Image, ImageDraw, ImageFont

from rgbmatrix import RGBMatrix, RGBMatrixOptions

HEIGHT, WIDTH = 32, 64

options = RGBMatrixOptions()
options.rows = HEIGHT
options.cols = WIDTH
options.chain_length = 2 
options.parallel = 1
options.hardware_mapping = "adafruit-hat"
options.show_refresh_rate = 0
options.limit_refresh_rate_hz = 100
options.brightness = 100
options.pixel_mapper_config = "U-mapper"

MATRIX = RGBMatrix(options=options)
CANVAS = MATRIX.CreateFrameCanvas()
IMAGE = Image.new("RGB", (WIDTH, HEIGHT))
DRAW = ImageDraw.Draw(IMAGE)
FONT = ImageFont.truetype("font.ttf", size=16)

def draw_clock():
    # RESET
    DRAW.rectangle(
        xy=[(0, 0), (WIDTH, HEIGHT)],
        fill=(0, 0, 0)
    )

    now = datetime.now(
        tz=timezone(offset=timedelta(hours=2))
    )
    year, month, day, hour, minute, second = now.year, now.month, now.day, now.hour, now.minute, now.second

    hours_angle = (hour % 12) / 12 * 360

    days_in_month = monthrange(year, month)[1]
    days_angle = (day / days_in_month) * 360

    MONTH_BOX   = [(11, 11), (20, 20)]
    DAY_BOX     = [( 8,  8), (23, 23)]
    HOUR_BOX    = [( 5,  5), (26, 26)]
    MINUTE_BOX  = [( 2,  2), (29, 29)]
    SECOND_BOX  = [( 0,  0), (31, 31)]

    # DRAW SECONDS
    if (minute % 2):
        # Opening Arc on odd minutes
        start, end = -90 + (second / 60) * 360, 270
    else:
       # Closing Arc on even minutes
        start, end = -90, -90 + (second / 60) * 360,

    DRAW.arc(
        xy=SECOND_BOX,
        start=start,
        end=end,
        # fill=(10, 110, 20),
        fill=(40, 40, 40),
        width=1
    )

    # DRAW MINUTES
    DRAW.arc(
        xy=MINUTE_BOX,
        start=-90,
        end=-90 + (minute / 60) * 360,
        # fill=(40,80,100),
        fill=(80, 80, 80),
        width=2
    )

    # DRAW HOURS
    DRAW.arc(
        xy=HOUR_BOX,
        start=-90,
        end=-90 + hours_angle,
        # fill=(130,91,0),
        fill=(200, 200, 200),
        width=2
    )

    # DRAW DAYS
    DRAW.arc(
        xy=DAY_BOX,
        start=-90,
        end=-90 + days_angle,
        # fill=(91,130,0),
        fill=(20, 20, 60),
        width=2
    )

    # DRAW MONTHS
    DRAW.pieslice(
        xy=MONTH_BOX,
        start=-90,
        end=-90 + (month / 12) * 360,
        # fill=(120, 120, 120)
        fill=(80, 80, 240)
    )

    # DRAW TIME AND DATE
    DRAW.text(
        xy=(35, 0),
        fill=(200, 200, 200),
        text=f"{hour:02d}:{minute:02d}",
        font=FONT
    )

    DRAW.text(
        xy=(35, 20),
        fill=(80, 80, 240),
        text=f"{day:02d}.{month:02d}.",
        font=FONT
    )

    CANVAS.SetImage(IMAGE, 0, 16) # X, Y
    MATRIX.SwapOnVSync(CANVAS, framerate_fraction=10)

try:
    while True:
        draw_clock()
        time.sleep(0.01)
except KeyboardInterrupt:
    sys.exit(0)
