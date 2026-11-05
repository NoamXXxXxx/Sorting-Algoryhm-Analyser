from visualiser import Bars, load_sort
import db
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QTableWidget, QTableWidgetItem, QMenuBar, QLineEdit, QSlider)
from PyQt6.QtCore import Qt


class AlgoAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        db.init_db()
        self.setWindowTitle("Sorting Algorythm Analyzer")
        self.setFixedSize(600, 400)

        self.stackedscreens = QStackedWidget()
        self.screens = [self.main_window(), self.about_window(), self.graph_visualiser_window(), self.database_window(), self.running_sort_window()]

        for screen in self.screens:
              self.stackedscreens.addWidget(screen)
        self.setCentralWidget(self.stackedscreens)

    def main_window(self): # main window
        window = QWidget()
        main_layout = QVBoxLayout()   
        btn_layout = QHBoxLayout()    
        bottom_layout = QHBoxLayout() 
        window.setLayout(main_layout)

        bar = QMenuBar()
        settings = bar.addMenu('Setting')
        about = bar.addAction('About')
        title = QLabel('Graph sort visualiser App')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        open_visualiser_btn = QPushButton("open visualiser")
        open_visualiser_btn.setFixedSize(300, 80)
        build = QLabel('Build 0.6')
        github = QLabel('<a href="https://github.com/NoamXXxXxx/Sorting-Algoryhm-Analyser">My Github</a>')
        github.setOpenExternalLinks(True)
        
        about.triggered.connect(lambda: self.stackedscreens.setCurrentIndex(1))
        open_visualiser_btn.clicked.connect(lambda: self.stackedscreens.setCurrentIndex(2))

        btn_layout.addStretch()
        btn_layout.addWidget(open_visualiser_btn)
        btn_layout.addStretch()
        bottom_layout.addWidget(build)
        bottom_layout.addStretch()
        bottom_layout.addWidget(github)
        main_layout.addWidget(bar)
        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)
        main_layout.addStretch()
        main_layout.addLayout(bottom_layout)

        return window

    def about_window(self): # about window
        window = QWidget()
        layout = QVBoxLayout()
        window.setLayout(layout)

        bar = QMenuBar()
        back = bar.addAction('Back')
        about = QLabel("about.md")
        about.setAlignment(Qt.AlignmentFlag.AlignCenter)

        back.triggered.connect(lambda: self.stackedscreens.setCurrentIndex(0))

        layout.addWidget(bar)
        layout.addWidget(about)
        layout.addStretch()

        return window

    def graph_visualiser_window(self): # pre-visualiser window
        window = QWidget()
        
        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        row_file = QHBoxLayout()
        row_db = QHBoxLayout()
        row_bars = QHBoxLayout()
        row_spread = QHBoxLayout()
        row_delay = QHBoxLayout()
        
        window.setLayout(main_layout)

        bar = QMenuBar()
        back = bar.addAction('back')
        settings = bar.addMenu('settings')
        title = QLabel('Graph visualiser')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_label = QLabel('sort function:')

        self.btn_choose_file = QPushButton('Choose file')
        self.btn_choose_file.setFixedWidth(150)
        
        self.db_label = QLabel('DB name:')
        self.db_input = QLineEdit()
        self.db_input.setPlaceholderText("Enter DB save name")
        self.db_input.setFixedWidth(150)

        self.bars_label = QLabel('bars amount:')
        self.bars_input = QLineEdit("50")
        self.bars_input.setPlaceholderText("e.g. 50")
        self.bars_input.setFixedWidth(150)
        self.spread_label = QLabel('numbers spread: 0')

        self.spread_slider = QSlider(Qt.Orientation.Horizontal)
        self.spread_slider.setMinimum(0)
        self.spread_slider.setMaximum(5)
        self.spread_slider.setFixedWidth(150)

        self.delay_label = QLabel('actions delay (ms):')
        self.delay_input = QLineEdit("5")
        self.delay_input.setPlaceholderText("e.g. 5")
        self.delay_input.setFixedWidth(150)

        run_file_btn = QPushButton("run file")
        run_file_btn.setFixedSize(150, 40)

        self.filename = QLabel('name: {filename}')

        time = QLabel('estemated running time: ...')

        open_db_btn = QPushButton("open database")
        open_db_btn.setFixedSize(150, 40)

        note = QLabel('note:\nvisualiser settings,\nas colors, and statistics\nare in settings tab')
        note.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self.spread_slider.valueChanged.connect(lambda val: self.spread_label.setText(f'numbers spread: {val}'))
        back.triggered.connect(lambda: self.stackedscreens.setCurrentIndex(0))
        open_db_btn.clicked.connect(lambda: self.stackedscreens.setCurrentIndex(3))
        self.btn_choose_file.clicked.connect(self.open_file_dialog)
        run_file_btn.clicked.connect(self.start_sort)

        row_file.addWidget(file_label)
        row_file.addStretch()
        row_file.addWidget(self.btn_choose_file)
        row_db.addWidget(self.db_label)
        row_db.addStretch()
        row_db.addWidget(self.db_input)
        row_bars.addWidget(self.bars_label)
        row_bars.addStretch()
        row_bars.addWidget(self.bars_input)
        row_spread.addWidget(self.spread_label)
        row_spread.addStretch()
        row_spread.addWidget(self.spread_slider) 
        row_delay.addWidget(self.delay_label)
        row_delay.addStretch()
        row_delay.addWidget(self.delay_input)
        left_layout.addLayout(row_file)
        left_layout.addLayout(row_db)
        left_layout.addLayout(row_bars)
        left_layout.addLayout(row_spread)
        left_layout.addLayout(row_delay)
        left_layout.addSpacing(20)
        left_layout.addWidget(run_file_btn)
        left_layout.addWidget(self.filename)
        left_layout.addWidget(time)
        left_layout.addStretch()
        left_layout.addWidget(open_db_btn)
        right_layout.addWidget(note)
        right_layout.addStretch()
        content_layout.addLayout(left_layout)
        content_layout.addStretch()
        content_layout.addLayout(right_layout)
        main_layout.addWidget(bar)
        main_layout.addWidget(title)
        main_layout.addSpacing(15)
        main_layout.addLayout(content_layout)

        return window

    def open_file_dialog(self): # choose file opener
        target_path = r"C:\Users\фыв\Desktop\project\sorting algorythms"
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file", target_path, "All Files (*)")
        if file_path:
            self.file_path = file_path
            self.filename.setText(f"sort function: {file_path.split('/')[-1]}")

    def database_window(self): # db window
        window = QWidget()
        layout = QVBoxLayout()
        self.table = QTableWidget()

        bar = QMenuBar()
        back = bar.addAction('back')

        back.triggered.connect(lambda: self.stackedscreens.setCurrentIndex(2))

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "File", "Bars", "Time ms", "Comparisons"])
        layout.addWidget(bar)
        layout.addWidget(self.table)
        window.setLayout(layout)

        return window
    
    def load_tier_list(self): # db load table
        rows = db.get_tier_list()
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))
                
    def start_sort(self): # start sorting
        sort_func = load_sort(self.file_path)
        self.chart.start(sort_func, int(self.bars_input.text()), int(self.delay_input.text()))
        self.stackedscreens.setCurrentIndex(4)

    def stop_and_back(self): # break sorting visualisation
        self.chart.timer.stop()
        self.stackedscreens.setCurrentIndex(2)

    def running_sort_window(self): #sorting window
        window = QWidget()
        layout = QVBoxLayout()
        window.setLayout(layout)

        self.chart = Bars()

        self.bar = QMenuBar()
        back = self.bar.addAction('Back')

        back.triggered.connect(lambda: self.stackedscreens.setCurrentIndex(2))

        label = QLabel("Running Sort Screen")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.bar)
        layout.addWidget(label)
        layout.addWidget(self.chart, 1)

        return window