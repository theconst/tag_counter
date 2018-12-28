import tkinter as tk
from typing import Dict, Union

import matplotlib.pyplot as plt
import numpy as np
from tk.matplot_to_tk import draw_figure


class HistogramWidget:
    items: Dict[str, int]
    xlabel: str
    ylabel: str
    figure: tk.PhotoImage
    canvas: tk.Canvas
    rotation: str

    def __init__(self, canvas: tk.Canvas,
                 items: Dict[str, int] = None,
                 title: str = '',
                 dpi: int = 100,
                 xlabel: str = '', ylabel: str = '',
                 rotation: Union[str, int] = 'vertical') -> None:
        self.xlabel = xlabel
        self.canvas = canvas
        self.ylabel = ylabel
        self.items = items
        self.rotation = rotation
        self.dpi = dpi
        self.title= title
        self.figure = None

    @property
    def width(self):
        if self.figure:
            return self.figure.width()
        raise ValueError('Figure not drawn')

    @property
    def height(self):
        if self.figure:
            return self.figure.height()
        raise ValueError('Figure not drawn')

    def draw(self):
        plt.clf()
        plt.figure(dpi=self.dpi)
        y_pos = np.arange(len(self.items))
        bar = plt.bar(y_pos, self.items.values())
        plt.xticks(y_pos, tuple(self.items.keys()), rotation=self.rotation)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)

        HistogramWidget._draw_numbers_on_bars(bar)

        plt.tight_layout()

        self.figure = draw_figure(self.canvas, plt.gcf())

    @staticmethod
    def _draw_numbers_on_bars(bar):
        for rect in bar:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2.0, height, int(height), ha='center', va='bottom')
