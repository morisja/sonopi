#!/usr/bin/env python3
from re import U
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import ST7789

display_type = "square"

# Create ST7789 LCD display class.

disp = ST7789.ST7789(
        height=240,
        rotation=0,
        port=0,
        cs=0,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
        dc=22,
        rst=27,
        backlight=19,               # 18 for back BG slot, 19 for front BG slot.
        spi_speed_hz=80 * 1000 * 1000,
        offset_left=0,
        offset_top=0
    )

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height


# Clear the display to a red background.
# Can pass any tuple of red, green, blue values (from 0 to 255 each).
# Get a PIL Draw object to start drawing on the display buffer.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))


# Load default font.
#font = ImageFont.load_default()

#f="PressStart2P.ttf"
# Alternatively load a TTF font.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Quicksand-Bold.ttf', 24)
#font = ImageFont.truetype('Open24DisplaySt.ttf', 24)

f="Monoid-Regular.ttf"

font = ImageFont.truetype(f, 18, layout_engine=ImageFont.LAYOUT_BASIC)

#18point font gives 8 rows, 19 chars each


def render_text(image, text_arr, position, font, fill=(255,255,255)):
    text="\n".join(text_arr)
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)

    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0, 0), text, font=font, fill=fill)
    # Rotate the text image.
    # rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    rotated=textimage
    image.paste(rotated, position, rotated)


summary=[]

class TextDisplay:
    def __init__(self, lines=9):
        self.n=0
        self.lines=lines
        self.x=0
        self.y=0
        self.s=0
    def get_buffer(self):
        out=[]
        for x in range(self.n, self.n+self.lines):
            p=str(x).zfill(3)
            out.append(f"{p}_abcdefghijklmno")
        self.n=self.n+1
        return out

    def get_sprite(self):
        xmax=19
        ymax=8
        out=[]
        p=[]
        # generate a huge list 
        for i in range(0,ymax*xmax):
            if i == self.s:
                p.append("X")
            else:
                p.append(" ")
                        
        i=0print(x._volume())

        #split that list by row
        for y in range(0,ymax):
            xrow=[]
            for x in range(0,xmax):
                xrow.append(p[i])
                i=i+1
            out.append("".join(xrow))

        self.s = self.s + 1
        return out



t=TextDisplay(9)

st=time.time()
frames=9*20
for p in range(1,frames):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((2, 2, WIDTH - 2, HEIGHT - 2), outline=(255, 255, 0), fill=(0, 0, 0))

    # Write two lines of white text on the buffer, rotated 90 degrees counter clockwise.
    #draw_rotated_text(img, 'Hello World!', (0, 0), 90, font, fill=(255, 255, 255))
    b=time.time()
    #render_text(img, t.get_buffer(), (6,15), font, (0,255,0))
    render_text(img, t.get_sprite(), (6,15), font, (0,255,0))
    #for n in range(1,2):
    #    draw_rotated_text(img, f"{p} This is a line of text.", (10, n*10*2), 0, font, fill=(255, 255, 255))
    e=time.time()
    d=e-b
    summary.append(f"text gen {d}")

    # Write buffer to display hardware, must be called to make things visible on the
    # display!
    disp.display(img)
et=time.time()

fps = frames/(et-st)
for s in summary:
    print(s)
print(f"fps {fps}")
