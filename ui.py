from visualiser import Bars, load_sort
import db

import os
import time
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QTableWidget, QTableWidgetItem,
    QMenuBar, QLineEdit, QMessageBox, QComboBox)
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import Qt, QUrl, QTimer


class AlgoAnalyzerApp(QMainWindow):
    def __init__(self): # init
        super().__init__()
        self.file_path = None
        db.init_db()
        self.setWindowTitle("Sorting Algorythm Analyzer")
        self.setFixedSize(700, 400)

        self.stackedscreens = QStackedWidget()
        self.screens = [self.main_window(), self.graph_visualiser_window(), self.database_window(), self.running_sort_window()]

        for screen in self.screens:
              self.stackedscreens.addWidget(screen)
        self.setCentralWidget(self.stackedscreens)

        self.chart.finished.connect(self.on_sort_finished)

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
        build = QLabel('Build 0.9')
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
        
        self.showstats = self.visualiser_settings.addAction('Show stats?')
        self.showstats.setCheckable(True)
        self.showstats.setChecked(True)
        
        self.visualiser_settings.addSeparator()
        
        self.colors_label = self.visualiser_settings.addAction('-----colors----- WIP') # WIP
        
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

        back.triggered.connect(lambda: self.stackedscreens.setCurrentIndex(0))
        open_db_btn.clicked.connect(lambda: self.stackedscreens.setCurrentIndex(2))
        open_db_btn.clicked.connect(lambda: self.load_tier_list())
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
        row_delay.addWidget(self.delay_label)
        row_delay.addStretch()
        row_delay.addWidget(self.delay_input)
        left_layout.addLayout(row_file)
        left_layout.addLayout(row_db)
        left_layout.addLayout(row_bars)
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
        h_layout = QHBoxLayout()
        self.table = QTableWidget()

        window.setLayout(layout)

        bar = QMenuBar()
        back = bar.addAction('back')
        self.delete_btn = QPushButton("Delete")
        self.delete_all_btn = QPushButton("Delete all")

        back.triggered.connect(lambda: self.stackedscreens.setCurrentIndex(1))
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_all_btn.clicked.connect(self.delete_all)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "File", "Bars", "Time sec", "Comparisons"])
        layout.addWidget(bar)
        layout.addWidget(self.table)
        h_layout.addWidget(self.delete_btn)
        h_layout.addStretch()
        h_layout.addWidget(self.delete_all_btn)
        layout.addLayout(h_layout)

        return window
    
    def load_tier_list(self): # db load table
        rows = db.get_tier_list()
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

    def delete_selected(self): # deletes selected row (id)
        row = self.table.currentRow()
        if row < 0:
            return
        rows = db.get_tier_list()
        db.delete_result(rows[row][0])
        self.load_tier_list()

    def delete_all(self): # deletes everything from db
        db.delete_all()
        self.load_tier_list()
                
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
            self.stats_timer.start(1)

        except ValueError as error:
            self.handle_error(error)
            return

        self.stackedscreens.setCurrentIndex(3)

    def stop_and_back(self): # break sorting visualisation
        self.chart.timer.stop()
        self.stackedscreens.setCurrentIndex(1)

    def update_stats(self): # stats + stats updater while sorting
        elapsed = (time.perf_counter() - self.chart.started_at)

        self.stats_label.setText(
            f"File: {os.path.basename(self.file_path)}  "
            f"Bars: {len(self.chart.arr)}    "
            f"Steps: {self.chart.steps}    "
            f"Time: {elapsed:.2f} sec    "
        )

        if not self.chart.timer.isActive():
            self.stats_timer.stop()

    def running_sort_window(self): # sorting window
        window = QWidget()
        h_layout = QHBoxLayout()
        layout = QVBoxLayout()
        window.setLayout(layout)

        self.stats_label = QLabel()

        self.stats_timer = QTimer(self)
        self.back_btn = QPushButton('Back')
        self.back_btn.setFixedSize(50, 30)
        self.chart = Bars()

        self.stats_label.setVisible(self.showstats.isChecked())
        self.showstats.toggled.connect(self.stats_label.setVisible)
        self.back_btn.clicked.connect(lambda: self.stackedscreens.setCurrentIndex(1))
        self.stats_timer.timeout.connect(self.update_stats)

        h_layout.addWidget(self.back_btn)
        h_layout.addStretch()
        h_layout.addWidget(self.stats_label)
        h_layout.addStretch()
        layout.addLayout(h_layout)
        layout.addWidget(self.chart, 1)

        return window

    def on_sort_finished(self, steps, elapsed_time): # stats save
        name = self.db_input.text()
        file = os.path.basename(self.file_path)
        self.file_path.split('/')[-1]
        bars_count = int(self.bars_input.text())
        
        db.save_res(name, file, bars_count, elapsed_time, steps)
        self.load_tier_list()








# add stats to running_sort_window, CSS (themes)