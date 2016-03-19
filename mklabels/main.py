import os
from argparse import ArgumentParser
from shutil import rmtree
from subprocess import STDOUT, check_output
from tempfile import mkdtemp
from textwrap import dedent

# A4 landscape
PAPER_WIDTH_MM = 297
PAPER_HEIGHT_MM = 210

STYLES = ['default', 'circles']


class ImpossibleLayout(Exception):
    pass


class TooManyLabels(Exception):
    pass


def quote_latex(s):
    charmap = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_':  r'\_',
        '{':  r'\{',
        '}':  r'\}',
        '~':  r'\textasciitilde{}',
        '^':  r'\^{}',
        '\\': r'\textbackslash{}',
    }

    return ''.join((charmap.get(c, c) for c in s))


def layout(page_width, page_height, margin, label_width, label_height,
           marker_length, marker_sep):
    rows = (page_height - 2 * margin) // \
        (label_height + 2 * marker_length + 2 * marker_sep)
    columns = (page_width - 2 * margin) // \
        (label_width + 2 * marker_length + 2 * marker_sep)

    if rows < 1 or columns < 1:
        raise ImpossibleLayout(
            'Not enough space on page to fit even one row or column')

    return (rows, columns)


def render(labels, margin, width, height, marker_length, marker_sep, debug,
           style):
    (rows, columns) = layout(PAPER_WIDTH_MM, PAPER_HEIGHT_MM, margin,
                             width, height, marker_length, marker_sep)

    if len(labels) > rows * columns:
        raise TooManyLabels('Cannot fit this many labels on the page')

    tex = dedent(r"""
        \documentclass{standalone}
        \usepackage[utf8]{inputenc}
        \usepackage[T1]{fontenc}

        \usepackage{tikz}
        \usetikzlibrary{calc}
        \tikzset{x=1mm,y=1mm}
        \pgfmathsetmacro{\margin}{%(margin)d}
        \pgfmathsetmacro{\markerlength}{%(marker_length)d}
        \pgfmathsetmacro{\markersep}{%(marker_sep)d}
        \pgfmathsetmacro{\labelwidth}{%(width)d}
        \pgfmathsetmacro{\labelheight}{%(height)d}

        \begin{document}
        \begin{tikzpicture}
        \useasboundingbox (0,0) rectangle (%(page_width)d,%(page_height)d);
    """) % {
        'margin': margin,
        'marker_length': marker_length,
        'marker_sep': marker_sep,
        'width': width,
        'height': height,
        'page_width': PAPER_WIDTH_MM,
        'page_height': PAPER_HEIGHT_MM,
    }

    x = 0
    y = 0

    for label in labels:
        tex += dedent(r"""
            \pgfmathsetmacro{\xpos}{\margin + %(x)d * (
              \labelwidth + 2 * \markerlength + 2 * \markersep)};
            \pgfmathsetmacro{\ypos}{\margin + %(y)d * (
              \labelheight + 2 * \markerlength + 2 * \markersep)};

            %(debug)s\draw[red] (\xpos,\ypos) rectangle
            %(debug)s  +(\labelwidth,\labelheight);
            %(debug)s\draw[blue] ($(\xpos,\ypos + 1/2 * \labelheight)$) --
            %(debug)s  +(\labelwidth,0);

        """) % {
            'x': x,
            'y': y,
            'debug': '' if debug else '%',
        }

        if style == 'default':
            tex += dedent(r"""
                \draw (\xpos,\ypos) ++(0,-\markersep) -- ++(0,-\markerlength);
                \draw (\xpos,\ypos) ++(-\markersep,0) -- ++(-\markerlength,0);

                \draw ($(\xpos,\ypos + \labelheight)$) ++(0,\markersep) --
                  ++(0,\markerlength);
                \draw ($(\xpos,\ypos + \labelheight)$) ++(-\markersep,0) --
                  ++(-\markerlength,0);

                \draw ($(\xpos + \labelwidth,\ypos)$) ++(0,-\markersep) --
                  ++(0,-\markerlength);
                \draw ($(\xpos + \labelwidth,\ypos)$) ++(\markersep,0) --
                  ++(\markerlength,0);

                \draw ($(\xpos + \labelwidth,\ypos + \labelheight)$)
                  ++(0,\markersep) -- ++(0,\markerlength);
                \draw ($(\xpos + \labelwidth,\ypos + \labelheight)$)
                  ++(\markersep,0) -- ++(\markerlength,0);
            """)
        else:
            tex += dedent(r"""
                \draw (\xpos,\ypos) -- ++(0,-\markersep) --
                  ++(0,-\markerlength);
                \draw (\xpos,\ypos) -- ++(-\markersep,0) --
                  ++(-\markerlength,0);
                \draw (\xpos,\ypos)
                  ++(0,\markerlength) arc (90:360:\markerlength);

                \draw ($(\xpos,\ypos + \labelheight)$) -- ++(0,\markersep) --
                  ++(0,\markerlength);
                \draw ($(\xpos,\ypos + \labelheight)$) -- ++(-\markersep,0) --
                  ++(-\markerlength,0);
                \draw ($(\xpos,\ypos + \labelheight)$)
                  ++(\markerlength,0) arc (0:270:\markerlength);

                \draw ($(\xpos + \labelwidth,\ypos)$) -- ++(0,-\markersep) --
                  ++(0,-\markerlength);
                \draw ($(\xpos + \labelwidth,\ypos)$) -- ++(\markersep,0) --
                  ++(\markerlength,0);
                \draw ($(\xpos + \labelwidth,\ypos)$)
                  ++(-\markerlength,0) arc (-180:90:\markerlength);

                \draw ($(\xpos + \labelwidth,\ypos + \labelheight)$) --
                  ++(0,\markersep) -- ++(0,\markerlength);
                \draw ($(\xpos + \labelwidth,\ypos + \labelheight)$) --
                  ++(\markersep,0) -- ++(\markerlength,0);
                \draw ($(\xpos + \labelwidth,\ypos + \labelheight)$)
                  ++(-\markerlength,0) arc (180:-90:\markerlength);
            """)

        tex += dedent(r"""
            \node[font=\sffamily\LARGE] at
              ($(\xpos + 1/2 * \labelwidth, \ypos + 1/2 * \labelheight)$)
              {\strut %(label)s};
        """) % {
            'label': quote_latex(label),
        }

        if (x + 1) < columns:
            x += 1
        else:
            x = 0
            y += 1

    tex += dedent(r"""
        \end{tikzpicture}
        \end{document}
    """)

    return tex


def compile_pdf(latex):
    directory = mkdtemp(prefix='mklabels-')
    try:
        os.chdir(directory)
        with file('labels.tex', 'w') as f:
            f.write(latex)
        check_output(
            ['pdflatex', '-halt-on-error', 'labels.tex'], stderr=STDOUT)
        check_output(['xdg-open', 'labels.pdf'])
    finally:
        rmtree(directory)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('labels', metavar='LABEL', nargs='+')
    parser.add_argument('--debug', '-d', action='store_true', help=''
                        'add debug guides to PDF output')
    parser.add_argument('--height', '-H', type=int, default=13, help=''
                        'height of the labels (mm)')
    parser.add_argument('--latex-only', '-t', action='store_true', help=''
                        'output latex code only; don\'t compile')
    parser.add_argument('--marker-length', '-l', type=int, default=2, help=''
                        'length of cut markers (mm)')
    parser.add_argument('--page-margin', '-m', type=int, default=15, help=''
                        'page margins of the whole page (mm)')
    parser.add_argument('--marker-sep', '-s', type=int, default=1, help=''
                        'marker distance to cut point (mm)')
    parser.add_argument('--style', '-S', default='default', choices=STYLES,
                        help='cutting guide style')
    parser.add_argument('--width', '-W', type=int, default=56, help=''
                        'width of the labels (mm)')

    return parser.parse_args()


def run():
    args = parse_args()
    output = render(
        args.labels, args.page_margin, args.width, args.height,
        args.marker_length, args.marker_sep, args.debug, args.style)

    if args.latex_only:
        print(output)
    else:
        compile_pdf(output)
