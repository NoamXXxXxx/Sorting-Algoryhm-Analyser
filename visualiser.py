import importlib.util
import random
import time

from PyQt6.QtCore import QRectF, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget


def load_sort(path):
    spec = importlib.util.spec_from_file_location("user_sort", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort


class Bars(QWidget):
    finished = pyqtSignal(int, float)

    def __init__(self):
        super().__init__()
        self.arr = []
        self.active = ()
        self.steps = 0
        self.gen = None
        self.started_at = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

    def start(self, sort_func, count, delay_ms):
        self.arr = random.sample(range(1, count + 1), count)
        self.steps = 0
        self.active = ()
        self.gen = sort_func(self.arr)
        self.started_at = time.perf_counter()
        self.timer.start(delay_ms)

    def step(self):
        try:
            self.active = next(self.gen)
            self.steps += 1
        except StopIteration:
            self.timer.stop()
            self.active = ()
            elapsed = (time.perf_counter() - self.started_at) * 1000
            self.finished.emit(self.steps, elapsed)
        self.update()

    def paintEvent(self, event):
        n = len(self.arr)
        if n == 0:
            return
        p = QPainter(self)
        p.setPen(Qt.PenStyle.NoPen)
        bar_w = self.width() / n
        top = max(self.arr)
        for i, value in enumerate(self.arr):
            bar_h = value / top * self.height()
            p.setBrush(QColor("red") if i in self.active else QColor("black"))
            p.drawRect(QRectF(i * bar_w, self.height() - bar_h, bar_w, bar_h))
        p.end()