import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QListWidget, 
                            QLabel, QSystemTrayIcon, QMenu, QTabWidget,
                            QTextEdit, QCalendarWidget, QListWidgetItem, QInputDialog, QMenu as QPopupMenu, QComboBox, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QPalette, QColor
from PIL import Image, ImageDraw, ImageFont, ImageColor
import win32gui
import win32con
import win32api
from datetime import datetime
import emoji
import json
import ctypes
from ctypes import wintypes

SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme = "dark"
        self.language = "vi"
        self.auto_wallpaper = False
        self.auto_clear_daily = False
        self.last_date = datetime.now().strftime('%Y-%m-%d')
        self.translations = {
            'vi': {
                'today': 'Công việc hôm nay:',
                'monthly': 'Mục tiêu tháng:',
                'longterm': 'Mục tiêu dài hạn:',
                'add_task': 'Thêm',
                'add_monthly': 'Thêm mục tiêu tháng',
                'add_longterm': 'Thêm mục tiêu dài hạn',
                'input_task': 'Nhập task mới...',
                'input_monthly': 'Nhập mục tiêu tháng...',
                'input_longterm': 'Nhập mục tiêu dài hạn...',
                'create_image': 'Tạo hình ảnh',
                'set_wallpaper': 'Đặt làm hình nền',
                'mark_done': 'Đánh dấu hoàn thành',
                'delete': 'Xóa',
                'title': 'Kế hoạch công việc',
                'tab_today': 'Công việc hôm nay',
                'tab_monthly': 'Mục tiêu tháng',
                'tab_longterm': 'Mục tiêu dài hạn',
            },
            'en': {
                'today': 'Today Tasks:',
                'monthly': 'Monthly Goals:',
                'longterm': 'Long-term Goals:',
                'add_task': 'Add',
                'add_monthly': 'Add Monthly Goal',
                'add_longterm': 'Add Long-term Goal',
                'input_task': 'Enter new task...',
                'input_monthly': 'Enter monthly goal...',
                'input_longterm': 'Enter long-term goal...',
                'create_image': 'Create Image',
                'set_wallpaper': 'Set as Wallpaper',
                'mark_done': 'Mark as Done',
                'delete': 'Delete',
                'title': 'Task Planner',
                'tab_today': 'Today',
                'tab_monthly': 'Monthly Goals',
                'tab_longterm': 'Long-term Goals',
            }
        }
        self.setWindowTitle("Task Manager")
        self.setMinimumSize(600, 700)
        self.setWindowIcon(QIcon(resource_path("assets/logo.ico")))
        
        # Top bar for theme and language
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Dark", "Light"])
        self.theme_box.currentIndexChanged.connect(self.change_theme)
        self.lang_box = QComboBox()
        self.lang_box.addItems(["Tiếng Việt", "English"])
        self.lang_box.currentIndexChanged.connect(self.change_language)
        self.auto_wallpaper_checkbox = QCheckBox("Tự động đặt hình nền khi thêm task")
        self.auto_wallpaper_checkbox.stateChanged.connect(self.toggle_auto_wallpaper)
        self.auto_clear_checkbox = QCheckBox("Tự động xóa task hôm nay khi sang ngày mới")
        self.auto_clear_checkbox.stateChanged.connect(self.toggle_auto_clear_daily)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        top_bar = QHBoxLayout()
        top_bar.addWidget(self.theme_box)
        top_bar.addWidget(self.lang_box)
        top_bar.addWidget(self.auto_wallpaper_checkbox)
        top_bar.addWidget(self.auto_clear_checkbox)
        layout.addLayout(top_bar)
        
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        daily_tab = QWidget()
        daily_layout = QVBoxLayout(daily_tab)
        
        # Tạo input field và nút thêm task
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText(self.translations[self.language]['input_task'])
        self.add_button = QPushButton(self.translations[self.language]['add_task'])
        self.add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)
        daily_layout.addLayout(input_layout)
        
        # Tạo list widget để hiển thị tasks
        self.task_list = QListWidget()
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.task_menu)
        daily_layout.addWidget(self.task_list)
        
        # Tab Monthly Goals
        monthly_tab = QWidget()
        monthly_layout = QVBoxLayout(monthly_tab)
        
        self.monthly_input = QLineEdit()
        self.monthly_input.setPlaceholderText(self.translations[self.language]['input_monthly'])
        self.monthly_add_btn = QPushButton(self.translations[self.language]['add_monthly'])
        self.monthly_add_btn.clicked.connect(self.add_monthly_goal)
        monthly_input_layout = QHBoxLayout()
        monthly_input_layout.addWidget(self.monthly_input)
        monthly_input_layout.addWidget(self.monthly_add_btn)
        monthly_layout.addLayout(monthly_input_layout)
        self.monthly_list = QListWidget()
        self.monthly_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.monthly_list.customContextMenuRequested.connect(self.monthly_goal_menu)
        monthly_layout.addWidget(self.monthly_list)
        
        # Tab Long-term Goals
        longterm_tab = QWidget()
        longterm_layout = QVBoxLayout(longterm_tab)
        
        self.longterm_input = QLineEdit()
        self.longterm_input.setPlaceholderText(self.translations[self.language]['input_longterm'])
        self.longterm_add_btn = QPushButton(self.translations[self.language]['add_longterm'])
        self.longterm_add_btn.clicked.connect(self.add_longterm_goal)
        longterm_input_layout = QHBoxLayout()
        longterm_input_layout.addWidget(self.longterm_input)
        longterm_input_layout.addWidget(self.longterm_add_btn)
        longterm_layout.addLayout(longterm_input_layout)
        self.longterm_list = QListWidget()
        self.longterm_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.longterm_list.customContextMenuRequested.connect(self.longterm_goal_menu)
        longterm_layout.addWidget(self.longterm_list)
        
        # Thêm các tab
        self.tab_widget.addTab(daily_tab, self.translations[self.language]['tab_today'])
        self.tab_widget.addTab(monthly_tab, self.translations[self.language]['tab_monthly'])
        self.tab_widget.addTab(longterm_tab, self.translations[self.language]['tab_longterm'])
        
        # Tạo nút để tạo hình ảnh và đặt làm hình nền
        button_layout = QHBoxLayout()
        self.create_image_button = QPushButton(self.translations[self.language]['create_image'])
        self.create_image_button.clicked.connect(self.create_task_image)
        self.set_wallpaper_button = QPushButton(self.translations[self.language]['set_wallpaper'])
        self.set_wallpaper_button.clicked.connect(self.set_wallpaper)
        button_layout.addWidget(self.create_image_button)
        button_layout.addWidget(self.set_wallpaper_button)
        layout.addLayout(button_layout)
        
        # Tạo system tray icon
        self.create_tray_icon()
        
        # Tạo thư mục để lưu hình ảnh nếu chưa tồn tại
        if not os.path.exists("images"):
            os.makedirs("images")
            
        # Tạo thư mục để lưu dữ liệu nếu chưa tồn tại
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Load dữ liệu đã lưu
        self.load_data()
        self.apply_theme()
        self.apply_language()
        self.auto_wallpaper_checkbox.setChecked(self.auto_wallpaper)
        self.auto_clear_checkbox.setChecked(self.auto_clear_daily)

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path("assets/icon.png")))
        self.tray_icon.setVisible(True)
        # Menu chuột phải
        tray_menu = QMenu()
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        open_action.triggered.connect(self.show_window_from_tray)
        exit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(open_action)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        # Click trái vào icon
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window_from_tray()

    def show_window_from_tray(self):
        self.showNormal()
        self.activateWindow()

    def add_task(self):
        self.check_and_clear_daily_tasks()
        task = self.task_input.text().strip()
        if task:
            item = QListWidgetItem(task)
            self.task_list.addItem(item)
            self.task_input.clear()
            self.save_data()
            if self.auto_wallpaper:
                self.set_wallpaper()

    def add_monthly_goal(self):
        text = self.monthly_input.text().strip()
        if text:
            item = QListWidgetItem(text)
            self.monthly_list.addItem(item)
            self.monthly_input.clear()
            self.save_data()

    def add_longterm_goal(self):
        text = self.longterm_input.text().strip()
        if text:
            item = QListWidgetItem(text)
            self.longterm_list.addItem(item)
            self.longterm_input.clear()
            self.save_data()

    def monthly_goal_menu(self, pos):
        item = self.monthly_list.itemAt(pos)
        if item:
            menu = QPopupMenu(self)
            mark_action = menu.addAction("Đánh dấu hoàn thành")
            delete_action = menu.addAction("Xóa mục tiêu")
            action = menu.exec(self.monthly_list.mapToGlobal(pos))
            if action == mark_action:
                font = item.font()
                font.setStrikeOut(not font.strikeOut())
                item.setFont(font)
                self.save_data()
            elif action == delete_action:
                self.monthly_list.takeItem(self.monthly_list.row(item))
                self.save_data()

    def longterm_goal_menu(self, pos):
        item = self.longterm_list.itemAt(pos)
        if item:
            menu = QPopupMenu(self)
            mark_action = menu.addAction("Đánh dấu hoàn thành")
            delete_action = menu.addAction("Xóa mục tiêu")
            action = menu.exec(self.longterm_list.mapToGlobal(pos))
            if action == mark_action:
                font = item.font()
                font.setStrikeOut(not font.strikeOut())
                item.setFont(font)
                self.save_data()
            elif action == delete_action:
                self.longterm_list.takeItem(self.longterm_list.row(item))
                self.save_data()

    def task_menu(self, pos):
        item = self.task_list.itemAt(pos)
        if item:
            menu = QPopupMenu(self)
            mark_action = menu.addAction("Đánh dấu hoàn thành")
            delete_action = menu.addAction("Xóa công việc")
            action = menu.exec(self.task_list.mapToGlobal(pos))
            if action == mark_action:
                font = item.font()
                font.setStrikeOut(not font.strikeOut())
                item.setFont(font)
                self.save_data()
            elif action == delete_action:
                self.task_list.takeItem(self.task_list.row(item))
                self.save_data()

    def save_data(self):
        data = {
            'theme': self.theme,
            'language': self.language,
            'auto_wallpaper': self.auto_wallpaper,
            'auto_clear_daily': self.auto_clear_daily,
            'last_date': self.last_date,
            'daily_tasks': [
                {'text': self.task_list.item(i).text(), 'done': self.task_list.item(i).font().strikeOut()}
                for i in range(self.task_list.count())
            ],
            'monthly_goals': [
                {'text': self.monthly_list.item(i).text(), 'done': self.monthly_list.item(i).font().strikeOut()}
                for i in range(self.monthly_list.count())
            ],
            'longterm_goals': [
                {'text': self.longterm_list.item(i).text(), 'done': self.longterm_list.item(i).font().strikeOut()}
                for i in range(self.longterm_list.count())
            ]
        }
        with open('data/tasks.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        try:
            with open('data/tasks.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.theme = data.get('theme', 'dark')
                self.language = data.get('language', 'vi')
                self.auto_wallpaper = data.get('auto_wallpaper', False)
                self.auto_clear_daily = data.get('auto_clear_daily', False)
                self.last_date = data.get('last_date', datetime.now().strftime('%Y-%m-%d'))
                self.theme_box.setCurrentIndex(0 if self.theme == 'dark' else 1)
                self.lang_box.setCurrentIndex(0 if self.language == 'vi' else 1)
                self.auto_wallpaper_checkbox.setChecked(self.auto_wallpaper)
                self.auto_clear_checkbox.setChecked(self.auto_clear_daily)
                # Load tasks
                for task in data.get('daily_tasks', []):
                    item = QListWidgetItem(task['text'])
                    if task.get('done'): item.setFont(self.strike_font(item.font()))
                    self.task_list.addItem(item)
                for goal in data.get('monthly_goals', []):
                    item = QListWidgetItem(goal['text'])
                    if goal.get('done'): item.setFont(self.strike_font(item.font()))
                    self.monthly_list.addItem(item)
                for goal in data.get('longterm_goals', []):
                    item = QListWidgetItem(goal['text'])
                    if goal.get('done'): item.setFont(self.strike_font(item.font()))
                    self.longterm_list.addItem(item)
            # GỌI check_and_clear_daily_tasks() SAU KHI ĐÃ LOAD TASK
            self.check_and_clear_daily_tasks()
        except FileNotFoundError:
            pass

    def strike_font(self, font):
        font.setStrikeOut(True)
        return font

    def save_and_quit(self):
        self.save_data()
        app.quit()

    def create_task_image(self):
        # Lấy kích thước màn hình
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        
        # Sử dụng theme cho hình ảnh
        bg_color = '#1e1e1e' if self.theme == 'dark' else '#f0f0f0'
        text_color = '#ffffff' if self.theme == 'dark' else '#222222'
        border_color = '#3d3d3d' if self.theme == 'dark' else '#cccccc'
        grid_color = '#2d2d2d' if self.theme == 'dark' else '#e0e0e0'
        
        # Tạo hình ảnh mới với kích thước màn hình và nền tối
        image = Image.new('RGB', (screen_width, screen_height), color=bg_color)
        draw = ImageDraw.Draw(image)
        
        # Sử dụng font Unicode (DejaVuSans.ttf) nếu có, nếu không thì dùng font mặc định
        try:
            font_path = resource_path("assets/DejaVuSans.ttf")
            title_font = ImageFont.truetype(font_path, 50)
            subtitle_font = ImageFont.truetype(font_path, 35)
            text_font = ImageFont.truetype(font_path, 30)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Vẽ tiêu đề lớn
        t = self.translations[self.language]
        draw.text((50, 50), f"{t['title']} - {datetime.now().strftime('%d/%m/%Y')}", fill=text_color, font=title_font)
        draw.line([(50, 120), (screen_width - 50, 120)], fill=border_color, width=3)
        # Tính toán vị trí các cột
        margin = 50
        col_width = (screen_width - 2 * margin) // 3
        col_x = [margin + i * col_width for i in range(3)]
        # Vẽ các tiêu đề mục theo hàng ngang
        y_title = 140
        draw.text((col_x[0], y_title), t['today'], fill='#ff6b6b', font=subtitle_font)
        draw.text((col_x[1], y_title), t['monthly'], fill='#4dabf7', font=subtitle_font)
        draw.text((col_x[2], y_title), t['longterm'], fill='#51cf66', font=subtitle_font)
        # Vẽ các task theo cột dọc bên dưới từng tiêu đề
        y_start = y_title + 50
        # Công việc hôm nay
        y = y_start
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            text = item.text()
            done = item.font().strikeOut()
            emoji = "☐" if not done else "☑"
            color = text_color if not done else '#888888'
            draw.text((col_x[0], y), f"{emoji} {text}", fill=color, font=text_font)
            y += 40
        # Mục tiêu tháng
        y = y_start
        for i in range(self.monthly_list.count()):
            item = self.monthly_list.item(i)
            text = item.text()
            done = item.font().strikeOut()
            emoji = "☐" if not done else "☑"
            color = text_color if not done else '#888888'
            draw.text((col_x[1], y), f"{emoji} {text}", fill=color, font=text_font)
            y += 40
        # Mục tiêu dài hạn
        y = y_start
        for i in range(self.longterm_list.count()):
            item = self.longterm_list.item(i)
            text = item.text()
            done = item.font().strikeOut()
            emoji = "☐" if not done else "☑"
            color = text_color if not done else '#888888'
            draw.text((col_x[2], y), f"{emoji} {text}", fill=color, font=text_font)
            y += 40
        # Vẽ khung trang trí
        draw.rectangle([(30, 30), (screen_width - 30, screen_height - 30)], 
                      outline=border_color, width=5)
        # Vẽ các đường trang trí
        for i in range(0, screen_width, 100):
            draw.line([(i, 30), (i, screen_height - 30)], fill=grid_color, width=1)
        for i in range(0, screen_height, 100):
            draw.line([(30, i), (screen_width - 30, i)], fill=grid_color, width=1)
        # Lưu hình ảnh
        image_path = os.path.join("images", "tasks.png")
        image.save(image_path)
        return image_path

    def set_wallpaper(self):
        try:
            image_path = self.create_task_image()
            # Chuyển đổi đường dẫn tương đối thành đường dẫn tuyệt đối
            abs_image_path = os.path.abspath(image_path)
            
            # Thử phương pháp 1: sử dụng win32gui
            try:
                win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, abs_image_path, 3)
            except:
                # Nếu phương pháp 1 thất bại, thử phương pháp 2: sử dụng ctypes
                user32 = ctypes.WinDLL('user32')
                SystemParametersInfo = user32.SystemParametersInfoW
                SystemParametersInfo.argtypes = ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint
                SystemParametersInfo.restype = ctypes.c_bool
                
                # Chuyển đổi đường dẫn thành chuỗi Unicode
                path = abs_image_path.encode('utf-16le') + b'\0'
                SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
        except Exception as e:
            print(f"Lỗi khi đặt hình nền: {str(e)}")

    def closeEvent(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Xác nhận")
        msg.setText("Bạn muốn làm gì?")
        quit_btn = msg.addButton("Tắt", QMessageBox.ButtonRole.AcceptRole)
        hide_btn = msg.addButton("Ẩn xuống tray", QMessageBox.ButtonRole.DestructiveRole)
        cancel_btn = msg.addButton("Hủy", QMessageBox.ButtonRole.RejectRole)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.exec()
        if msg.clickedButton() == quit_btn:
            self.save_data()
            event.accept()
            QApplication.quit()
        elif msg.clickedButton() == hide_btn:
            event.ignore()
            self.hide()
        else:
            event.ignore()

    def change_theme(self, idx):
        self.theme = "dark" if idx == 0 else "light"
        self.apply_theme()
        self.save_data()

    def change_language(self, idx):
        self.language = "vi" if idx == 0 else "en"
        self.apply_language()
        self.save_data()

    def apply_theme(self):
        if self.theme == "dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #1e1e1e; }
                QWidget { background-color: #1e1e1e; color: #ffffff; }
                QTabWidget::pane { border: 1px solid #3d3d3d; background-color: #1e1e1e; }
                QTabBar::tab { background-color: #2d2d2d; color: #ffffff; padding: 8px 16px; border: 1px solid #3d3d3d; }
                QTabBar::tab:selected { background-color: #3d3d3d; }
                QLineEdit, QTextEdit { background-color: #2d2d2d; color: #ffffff; border: 1px solid #3d3d3d; padding: 5px; }
                QPushButton { background-color: #0d47a1; color: white; border: none; padding: 8px 16px; border-radius: 4px; }
                QPushButton:hover { background-color: #1565c0; }
                QListWidget { background-color: #2d2d2d; color: #ffffff; border: 1px solid #3d3d3d; }
                QListWidget::item { padding: 5px; }
                QListWidget::item:selected { background-color: #3d3d3d; }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #f0f0f0; }
                QWidget { background-color: #f0f0f0; color: #222222; }
                QTabWidget::pane { border: 1px solid #cccccc; background-color: #f0f0f0; }
                QTabBar::tab { background-color: #e0e0e0; color: #222222; padding: 8px 16px; border: 1px solid #cccccc; }
                QTabBar::tab:selected { background-color: #ffffff; }
                QLineEdit, QTextEdit { background-color: #ffffff; color: #222222; border: 1px solid #cccccc; padding: 5px; }
                QPushButton { background-color: #1976d2; color: white; border: none; padding: 8px 16px; border-radius: 4px; }
                QPushButton:hover { background-color: #42a5f5; }
                QListWidget { background-color: #ffffff; color: #222222; border: 1px solid #cccccc; }
                QListWidget::item { padding: 5px; }
                QListWidget::item:selected { background-color: #e0e0e0; }
            """)

    def apply_language(self):
        t = self.translations[self.language]
        self.task_input.setPlaceholderText(t['input_task'])
        self.add_button.setText(t['add_task'])
        self.monthly_input.setPlaceholderText(t['input_monthly'])
        self.monthly_add_btn.setText(t['add_monthly'])
        self.longterm_input.setPlaceholderText(t['input_longterm'])
        self.longterm_add_btn.setText(t['add_longterm'])
        self.create_image_button.setText(t['create_image'])
        self.set_wallpaper_button.setText(t['set_wallpaper'])
        self.tab_widget.setTabText(0, t['tab_today'])
        self.tab_widget.setTabText(1, t['tab_monthly'])
        self.tab_widget.setTabText(2, t['tab_longterm'])

    def toggle_auto_wallpaper(self, state):
        self.auto_wallpaper = bool(state)
        self.save_data()

    def toggle_auto_clear_daily(self, state):
        self.auto_clear_daily = bool(state)
        self.save_data()

    def check_and_clear_daily_tasks(self):
        today = datetime.now().strftime('%Y-%m-%d')
        if self.auto_clear_daily and self.last_date != today:
            if self.task_list.count() > 0:
                self.task_list.clear()
                self.last_date = today
                self.save_data()
            else:
                self.last_date = today

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec()) 