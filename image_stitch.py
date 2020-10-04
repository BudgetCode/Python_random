import time
import string
from os import listdir
from os.path import abspath, dirname, isfile, join

from PIL import Image

VALID_FORMATS = ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp')
VALID_CHARS = set("-_.() %s%s" % (string.ascii_letters, string.digits))
DIRECTORY = dirname(abspath(__file__))
OFFSET = 5


def names_to_image(file_names):
    return [Image.open(name) for name in file_names]


def hstack(images):
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths) + OFFSET * len(images)
    max_height = max(heights)

    stitched = Image.new('RGBA', (total_width, max_height))
    x_offset = 0
    for im in images:
        stitched.paste(im, (x_offset, 0))
        x_offset += im.size[0] + OFFSET
    return stitched


def vstack(images):
    widths, heights = zip(*(i.size for i in images))
    total_height = sum(heights) + OFFSET * len(images)
    max_width = max(widths)
    stitched = Image.new('RGBA', (max_width, total_height))
    y_offset = 0
    for im in images:
        x_offset = (max_width - im.size[0]) // 2
        stitched.paste(im, (x_offset, y_offset))
        y_offset += im.size[1] + OFFSET
    return stitched


def stitch(file_names, x):
    global directroy
    total_files = len(file_names)

    sections = [names_to_image(file_names[n:n + x])
                if n + x <= total_files
                else names_to_image(file_names[n: total_files])
                for n in range(0, total_files, x)]

    stitched = [hstack(images) for images in sections]
    name = input("\nEnter the Image name to be Saved As, Existing File Name will be overwritten > ")
    if not (name and set(name) & VALID_CHARS):
        name = 'result'

    vstack(stitched).save(join(DIRECTORY, f'{name}.png'))

    return name


def main():
    print("""
            Enter Max horizonatal Stitch Limit , i.e 2 or 5 , Images will stacked vertically if more.

                            > Example | [ LIMIT = 3 ] and [ No of Images = 8 ] <

                                                | X  X  X |
                                                | X  X  X |
                                                |  X   X  |
          """)
    x = -1
    while True:
        try:
            x = int(input('Stitch limit > '))
            assert x >= 1
        except (KeyError, AssertionError):
            print("\nERROR: Invalid Input, Limit must greater than or equal to 1.\n")
        else:
            break
    file_names = [join(DIRECTORY, f) for f in listdir(DIRECTORY)
                  if isfile(join(DIRECTORY, f)) and f.endswith(VALID_FORMATS)]

    if not file_names:
        print(f"\nERROR: No Images Found in the Current Directory: {DIRECTORY}\n")

    else:
        start = time.perf_counter()
        name = stitch(file_names, x)
        duration = time.perf_counter() - start
        print(f"\nResult Image Saved as '{name}.png' | Stitch Time : {duration:.2f}s")

    input()
    return


main()
