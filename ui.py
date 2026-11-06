from visualiser import Bars, load_sort
import db
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QTableWidget, QTableWidgetItem,
    QMenuBar, QLineEdit, QSlider, QMessageBox, QComboBox)
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import Qt, QUrl


class AlgoAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = None
        db.init_db()
        self.setWindowTitle("Sorting Algorythm Analyzer")
        self.setFixedSize(600, 400)

        self.stackedscreens = QStackedWidget()
        self.screens = [self.main_window(), self.graph_visualiser_window(), self.database_window(), self.running_sort_window()]

        for screen in self.screens:
              self.stackedscreens.addWidget(screen)
        self.setCentralWidget(self.stackedscreens)

    def main_window(self): # main window
        window = QWidget()
        main_layout = QVBoxLayout()   
        btn_layout = QHBoxLayout()    
        bottom_layout = QHBoxLayout() 
        window.setLayout(main_layout)

        self.bar = QMenuBar()
        self.settings = self.bar.addMenu('Setting')
        self.settings_combo(self.settings)
        about = self.bar.addAction('About')

        title = QLabel('Graph sort visualiser App')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        open_visualiser_btn = QPushButton("open visualiser")
        open_visualiser_btn.setFixedSize(300, 80)
        build = QLabel('Build 0.7.1')
        github = QLabel('<a href="https://github.com/NoamXXxXxx/Sorting-Algoryhm-Analyser">My Github</a>')
        github.setOpenExternalLinks(True)
        
        about.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/NoamXXxXxx/Sorting-Algoryhm-Analyser/blob/main/about.md")))
        open_visualiser_btn.clicked.connect(lambda: self.stackedscreens.setCurrentIndex(1))

        btn_layout.addStretch()
        btn_layout.addWidget(open_visualiser_btn)
        btn_layout.addStretch()
        bottom_layout.addWidget(build)
        bottom_layout.addStretch()
        bottom_layout.addWidget(github)
        main_layout.addWidget(self.bar)
        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)
        main_layout.addStretch()
        main_layout.addLayout(bottom_layout)

        return window

    def settings_combo(self, menu_object): # open settings
        menu_object.addAction('theme: light')
        self.visualiser_settings = menu_object.addMenu('Visualiser settings')
        
        self.stat_label = self.visualiser_settings.addAction('-----statistics-----')
        
        self.act_file_name = self.visualiser_settings.addAction('file name')
        self.act_file_name.setCheckable(True)
        self.act_file_name.setChecked(True)
        
        self.act_comparisons = self.visualiser_settings.addAction('comparisons count')
        self.act_comparisons.setCheckable(True)
        self.act_comparisons.setChecked(True)
        
        self.act_accesses = self.visualiser_settings.addAction('array accesses')
        self.act_accesses.setCheckable(True)
        self.act_accesses.setChecked(True)
        
        self.act_action_delay = self.visualiser_settings.addAction('action delay')
        self.act_action_delay.setCheckable(True)
        self.act_action_delay.setChecked(True) 
        
        self.visualiser_settings.addSeparator()
        
        self.colors_label = self.visualiser_settings.addAction('-----colors-----')
        
        self.act_bar_color = self.visualiser_settings.addAction('bar color: {HEX}')
        self.act_selected_color = self.visualiser_settings.addAction('selected bar color: {HEX}')
        self.act_final_color = self.visualiser_settings.addAction('final bars color: {HEX}')


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
        self.settings_combo(settings)
        title = QLabel('Graph visualiser')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_label = QLabel('File:')

        self.btn_choose_file = QPushButton('Choose file')
        self.btn_choose_file.setFixedWidth(150)
        self.filename = QLabel('File: ...')

        self.db_label = QLabel('DB name:')
        self.db_input = QLineEdit()
        self.db_input.setPlaceholderText("Enter DB save name")
        self.db_input.setFixedWidth(150)

        self.bars_label = QLabel('bars amount:')
        self.bars_input = QLineEdit()
        self.bars_input.setPlaceholderText("e.g. 50")
        self.bars_input.setFixedWidth(150)
        self.spread_label = QLabel('numbers spread: 0')

        self.spread_slider = QSlider(Qt.Orientation.Horizontal)
        self.spread_slider.setMinimum(0)
        self.spread_slider.setMaximum(5)
        self.spread_slider.setFixedWidth(150)

        self.delay_label = QLabel('actions delay (ms):')
        self.delay_input = QLineEdit()
        self.delay_input.setPlaceholderText("e.g. 5")
        self.delay_input.setFixedWidth(150)

        run_file_btn = QPushButton("run file")
        run_file_btn.setFixedSize(150, 40)

        open_db_btn = QPushButton("open database")
        open_db_btn.setFixedSize(150, 40)

        note = QLabel('note:\nvisualiser settings,\nas colors, and statistics\nare in settings tab')
        note.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self.spread_slider.valueChanged.connect(lambda val: self.spread_label.setText(f'numbers spread: {val}'))
        back.triggered.connect(lambda: self.stackedscreens.setCurrentIndex(0))
        open_db_btn.clicked.connect(lambda: self.stackedscreens.setCurrentIndex(2))
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

    def handle_error(self, error): # error handler
        QMessageBox.warning(self, "Input error", str(error))

    def open_file_dialog(self): # choose file opener
        target_path = r"C:\Users\фыв\Desktop\project\sorting algorythms"
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file", target_path, "All Files (*)")
        if file_path:
            self.file_path = file_path
            self.filename.setText(f"File: {file_path.split('/')[-1]}")

    def database_window(self): # db window
        window = QWidget()
        layout = QVBoxLayout()
        self.table = QTableWidget()

        bar = QMenuBar()
        back = bar.addAction('back')

        back.triggered.connect(lambda: self.stackedscreens.setCurrentIndex(1 ))

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
                
    def start_sort(self): # start sorting + error handler
        if not self.file_path:
            self.handle_error("Choose file first")
            return
        if not self.bars_input.text().strip():
            self.handle_error("Enter bars amount first")
            return
        
        if not self.delay_input.text().strip():
            self.handle_error("Enter delay first")
            return
        
        try:
            bars = int(self.bars_input.text())
            delay = int(self.delay_input.text())

            if bars <= 0:
                raise ValueError("Bars amount must be greater than 0")
            if delay < 0:
                raise ValueError("Delay cannot be negative")

            sort_func = load_sort(self.file_path)
            self.chart.start(sort_func, bars, delay)

        except ValueError as error:
            self.handle_error(error)
            return

        self.stackedscreens.setCurrentIndex(3)

    def stop_and_back(self): # break sorting visualisation
        self.chart.timer.stop()
        self.stackedscreens.setCurrentIndex(1)

    def running_sort_window(self): #sorting window
        window = QWidget()
        layout = QVBoxLayout()
        window.setLayout(layout)

        self.chart = Bars()

        self.back_btn = QPushButton('Back')
        self.back_btn.setFixedSize(50, 30)

        self.back_btn.clicked.connect(lambda: self.stackedscreens.setCurrentIndex(1))

        layout.addWidget(self.back_btn)
        layout.addWidget(self.chart, 1)

        return window








# add stats to running_sort_window, CSS (themes), db saves