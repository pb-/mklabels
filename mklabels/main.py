from argparse import ArgumentParser


class NotEnoughSpace(Exception):
    pass


def layout(page_width, page_height, margin, label_width, label_height,
           marker_length, marker_sep):
    rows = (page_height - 2 * margin) // \
        (label_height + 2 * marker_length + 2 * marker_sep)
    columns = (page_width - 2 * margin) // \
        (label_width + 2 * marker_length + 2 * marker_sep)

    if rows < 1 or columns < 1:
        raise NotEnoughSpace(
            'Not enough space on page to fit even one row or column!')

    return (rows, columns)


def render(labels, margin, width, height, marker_length, marker_sep):
    pass


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--height', '-H', type=int, default=13, help=''
                        'height of the labels (mm)')
    parser.add_argument('--latex', '-t', action='store_true', help=''
                        'output latex code only; don\'t compile')
    parser.add_argument('--marker-length', '-l', type=int, default=2, help=''
                        'length of cut markers (mm)')
    parser.add_argument('--page-margin', '-m', type=int, default=15, help=''
                        'page margins of the whole page (mm)')
    parser.add_argument('--marker-sep', '-s', type=int, default=1, help=''
                        'marker distance to cut point (mm)')
    parser.add_argument('--width', '-W', type=int, default=56, help=''
                        'width of the labels (mm)')

    return parser.parse_args()


def run():
    args = parse_args()
