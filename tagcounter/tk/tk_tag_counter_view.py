import tkinter as tk
import tkinter.filedialog
from typing import Union, List

import log
from model.entities import Site
from tk.histogram_widget import HistogramWidget
from model.tag_counter_model import TagCounterModel
from tag_counter_view import TagCounterView

logger = log.get_logger(__name__)


class TkTagCounterView(TagCounterView):

    _ROTATION = -90
    _REFRESH_INTERVAL_MILLIS = 2000
    _WHOLE_ROW = 'WE'
    _IMMEDIATE = 0
    _DEFERRED = 10

    root: tk.BaseWidget
    _tag_counter_model: TagCounterModel

    menu: tk.Menu
    manual_choice_entry: tk.Entry
    alternatives_lb: tk.Listbox
    submit_button: tk.Button
    histogram_window: tk.Toplevel = None

    _histogram: HistogramWidget = None

    _choice: str = None

    _queue: List[str]

    _running: bool

    def __init__(self, tag_counter_model: TagCounterModel):
        TagCounterView.__init__(self, tag_counter_model)

        master = self.root = tk.Tk()

        self._tag_counter_model = tag_counter_model

        self._running = False

        self.menu = tk.Menu()
        self.menu.add_command(label='Alias...', command=self._choose_file)
        master.config(menu=self.menu)

        self.manual_choice_entry = tk.Entry(master)
        self.manual_choice_entry.bind('<KeyRelease>', self._update_from_entry)
        self.manual_choice_entry.bind('<Return>', self._submit)
        self.manual_choice_entry.grid(row=0, sticky=TkTagCounterView._WHOLE_ROW)

        self.alternatives_fr = tk.Frame(master)
        self.alternatives_lb = tk.Listbox(self.alternatives_fr, selectmode=tk.SINGLE)
        self.alternatives_lb.bind('<Return>', self._submit)
        self.alternatives_lb.bind('<<ListboxSelect>>', self._update_from_lb)
        self.alternatives_lb.bind('<Double-Button-1>', self._submit)
        self.alternatives_lb.pack(side=tk.LEFT, fill=tk.Y)
        self.alternatives_sb = tk.Scrollbar(self.alternatives_fr, orient=tk.VERTICAL)
        self.alternatives_sb.config(command=self.alternatives_lb.yview)
        self.alternatives_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.alternatives_fr.grid(row=1, sticky=TkTagCounterView._WHOLE_ROW)

        self.submit_button = tk.Button(text='Submit', command=self._submit)
        self.submit_button.grid(row=2, sticky=TkTagCounterView._WHOLE_ROW)

        self.status_bar_text = tk.StringVar()
        self.status_bar = tk.Label(textvariable=self.status_bar_text)
        self.status_bar.grid(row=3, sticky=TkTagCounterView._WHOLE_ROW)

        self._tag_counter_model.on_url_added += self._add_alternative
        self._tag_counter_model.on_site_refreshed += self._display_site_info
        self._tag_counter_model.on_error += self._display_error

    def activate(self):
        self.root.mainloop()

    def _choose_file(self):
        file_name = tk.filedialog.askopenfilename()
        if file_name:
            self.on_input_file_selected(file_name)

    def _display_error(self, error: Union[str, Exception]) -> None:
        if isinstance(error, Exception):
            logger.error(error, exc_info=True)
            self._show_fading_status("Error occurred...")
        self._show_fading_status(error)

    def _submit(self, *_) -> None:
        self.root.after(TkTagCounterView._IMMEDIATE, lambda: self._show_fading_status("Loading..."))
        self.root.after(TkTagCounterView._DEFERRED, lambda: self.on_input_submitted(self._choice))

    def _show_fading_status(self, status: str):
        self.status_bar_text.set(status)
        self.root.after(self._REFRESH_INTERVAL_MILLIS, self._clear_status_bar)

    def _clear_status_bar(self):
        self.status_bar_text.set('')

    def _display_site_info(self, site: Site) -> None:
        if self.histogram_window:
            self.histogram_window.destroy()
        self.histogram_window = tk.Toplevel(self.root)
        self.histogram_window.wm_title(site.url)

        frame = tk.Frame(self.histogram_window)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._histogram = HistogramWidget(
            canvas,
            items=site.tag_histogram.as_counter(),
            title=site.url,
            xlabel='Tags',
            ylabel='Frequency',
            rotation=TkTagCounterView._ROTATION)
        self._histogram.draw()

        dimensions = "{}x{}".format(self._histogram.width, self._histogram.height)
        self.histogram_window.geometry(dimensions)

    def _update_from_entry(self, _) -> None:
        entry_text = self.manual_choice_entry.get()
        if entry_text:
            self._choice = entry_text.strip()
            self.on_refresh_selected(refresh=True)

    def _update_from_lb(self, _) -> None:
        selection = self.alternatives_lb.curselection()
        if selection:
            self._choice = self.alternatives_lb\
                .get(selection)\
                .strip()
            self.on_refresh_selected(refresh=False)

    def _add_alternative(self, url: str) -> None:
        self.alternatives_lb.insert(tk.END, url)
