#!python

import argparse

import requests
from matplotlib import cm


def range_limited_float_type(min_v, max_v):
    def custom_type(arg):
        """ Type function for argparse - a float within some predefined bounds """
        try:
            f = float(arg)
        except ValueError:
            raise argparse.ArgumentTypeError("Must be a floating point number")
        if f < min_v or f > max_v:
            raise argparse.ArgumentTypeError(f"Argument must be < {str(max_v)} and > {str(min_v)}")
        return f
    return custom_type


def to_hex(v):
    o = hex(v)[2:]
    if len(o) < 2:
        return '0' + o
    else:
        return o


def apply_color_array(url, color_array):
    print(requests.post(f"{url}/set_led_strip", {"color_array": ','.join(color_array)}))


def set_static_color(url, color, pixel_quantity, brightness=1):
    color_chunks = [color[i:i+2] for i in range(0, len(color), 2)]
    color = ''.join([to_hex(round(int(chunk, 16)*brightness)) for chunk in color_chunks])
    apply_color_array(url, [color for _ in range(pixel_quantity)])


def display_rainbow(url, pixel_quantity, offset=0, brightness=1):
    hue = cm.get_cmap('hsv', pixel_quantity)
    color_array = []
    for i in range(pixel_quantity):
        i = i + offset
        if i > pixel_quantity:
            i = i - pixel_quantity
        color_array.append("00" + ''.join([to_hex(round(v * 255 * brightness)) for v in hue(i / pixel_quantity)][:-1]))
    apply_color_array(url, color_array)


def rainbow_mode(url, pixel_quantity, speed=1, brightness=1):
    i = 0
    while True:
        i += 1
        if i > pixel_quantity:
            i -= pixel_quantity
        display_rainbow(url, pixel_quantity, i, brightness)


def main(args):
    if args.mode == "static_color":
        if args.color is None:
            parser.error("static_color mode requires --color")
        set_static_color(args.host, args.color, args.pq, args.brightness)
    elif args.mode == "rainbow":
        rainbow_mode(args.host, args.pq, args.speed, args.brightness)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"""
        Sets static color to led strip.
    """)
    parser.add_argument('--mode', type=str, help="mode", choices=["static_color", "static_rainbow", "rainbow"],
                        required=True)
    parser.add_argument('--color', type=str, help="hex color in format wwrrggbb")
    parser.add_argument('--brightness', type=range_limited_float_type(0, 1), default=1)
    parser.add_argument('--speed', type=range_limited_float_type(0, 1), help="hex color in format wwrrggbb", default=1)
    parser.add_argument('--host', type=str, help="host address of led strip", required=True)
    parser.add_argument('--pq', type=int, help="led strip pixel quantity", default=150)

    main(parser.parse_args())
