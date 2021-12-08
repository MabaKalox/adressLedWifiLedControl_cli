import argparse

import requests
from matplotlib import cm


def to_hex(v):
    o = hex(v)[2:]
    if len(o) < 2:
        return '0' + o
    else:
        return o


def apply_color_array(url, color_array):
    print(requests.post(f"{url}/set_led_strip", {"color_array": ','.join(color_array)}))


def set_static_color(url, color, pixel_quantity):
    apply_color_array(url, [color for _ in range(pixel_quantity)])


def display_rainbow(url, pixel_quantity, offset=0):
    hue = cm.get_cmap('hsv', pixel_quantity)
    color_array = []
    for i in range(pixel_quantity):
        i = i + offset
        if i > pixel_quantity:
            i = i - pixel_quantity
        color_array.append("00" + ''.join([to_hex(round(v * 255)) for v in hue(i / pixel_quantity)][:-1]))
    apply_color_array(url, color_array)


def rainbow_mode(url, pixel_quantity, speed=1):
    i = 0
    while True:
        i += 1
        if i > pixel_quantity:
            i -= pixel_quantity
        display_rainbow(url, pixel_quantity, i)


def main(args):
    if args.mode == "static_color":
        if args.color is None:
            parser.error("static_color mode requires --color")
        set_static_color(args.host, args.color, args.pq)
    elif args.mode == "rainbow":
        if args.speed > 1 or args.speed < 0:
            parser.error("--speed should be between 0 and 1")
        rainbow_mode(args.host, args.pq, args.speed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"""
        Sets static color to led strip.
    """)
    parser.add_argument('--mode', type=str, help="mode", choices=["static_color", "static_rainbow", "rainbow"],
                        required=True)
    parser.add_argument('--color', type=str, help="hex color in format wwrrggbb")
    parser.add_argument('--speed', type=float, help="hex color in format wwrrggbb", default=1)
    parser.add_argument('--host', type=str, help="host address of led strip", required=True)
    parser.add_argument('--pq', type=int, help="led strip pixel quantity", default=150)

    main(parser.parse_args())
