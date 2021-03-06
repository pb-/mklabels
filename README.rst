========
mklabels
========

``mklabels`` generates a printable PDF sheet of labels with cutting guides.

Sometimes you simply want to label stuff in a consistent way.
For example folders, spices, drawers, doorbell signs, ... you name it.
With ``mklabels`` you can prepare a PDF file with labels of specified size including cutting guides that help you to cut out the individual labels.


Installation
------------
::

  pip install git+git://github.com/pb-/mklabels

You will also need the ``pdflatex`` LaTeX compiler and the ``standalone`` document class as well as the ``tikz`` package.
On a Debian-like distribution, installing the ``texlive-latex-extra`` package should suffice.


Usage
-----

Running
::

  mklabels Work Insurance Home

produces something like this (cropped for presentation):

.. image:: doc/example.png

For more options check out ``mklabels --help``.
