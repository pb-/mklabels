from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--height', '-H', type=int, default=12, help=''
                        'height of the labels (mm)')
    parser.add_argument('--marker-length', '-l', type=int, default=2, help=''
                        'length of cut markers (mm)')
    parser.add_argument('--marker-sep', '-s', type=int, default=1, help=''
                        'marker distance to cut point (mm)')
    parser.add_argument('--page-margin', '-m', type=int, default=15, help=''
                        'page margins of the whole page (mm)')
    parser.add_argument('--width', '-W', type=int, default=57, help=''
                        'width of the labels (mm)')

    return parser.parse_args()


def run():
    args = parse_args()
