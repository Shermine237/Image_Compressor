#   Design Widget
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QListWidget, QTextEdit,\
    QPushButton, QToolBar, QTreeView, QListView, QSlider, QHBoxLayout, QVBoxLayout, QSpinBox,\
    QLineEdit, QAbstractItemView, QListWidgetItem, QMessageBox, QProgressDialog
from PySide6.QtCore import QSize, QItemSelectionModel, QStandardPaths, Qt, QThread, QObject
from PySide6.QtGui import QIcon, QShortcut, QKeySequence


class Application(QApplication):
    def __init__(self):
        super().__init__()


class HBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)


class Icon(QIcon):
    def __init__(self, path):
        super().__init__(path)


class ItemSelectionModel(QItemSelectionModel):
    def __init__(self):
        super().__init__()


class KeySequence(QKeySequence):
    def __init__(self, key):
        super().__init__(key)


class Label(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)


class LineEdit(QLineEdit):
    def __init__(self, text_holder):
        super().__init__()
        self.setPlaceholderText(text_holder)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)


class ListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.setAlternatingRowColors(True)


class ListWidgetItem(QListWidgetItem):
    def __init__(self, name):
        super().__init__(name)


class ListView(QListView):
    def __init__(self):
        super().__init__()
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setUniformItemSizes(True)
        self.setIconSize(QSize(60, 60))

    # Methods
    def set_icon_size(self, b, h):
        self.setIconSize(QSize(b, h))


class MainWidget(QWidget):
    def __init__(self, title, b=600, h=500):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(b, h)


class MainWindows(QMainWindow):
    def __init__(self, title, b=600, h=500):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(b, h)

        self.central_widget = QWidget()
        self.toolbar = QToolBar()

        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.central_widget)


class MessageBoxCritical(QMessageBox):
    def __init__(self, titre, text):
        super().__init__(QMessageBox.Icon.Critical, titre, text)


class MessageBoxWarning(QMessageBox):
    def __init__(self, titre, text):
        super().__init__(QMessageBox.Icon.Warning, titre, text)


class Object(QObject):
    def __init__(self):
        super().__init__()


class ProgressDialog(QProgressDialog):
    def __init__(self, title, button_text, start_number, end_number):
        super().__init__(title, button_text, start_number, end_number)


class PushButton(QPushButton):
    def __init__(self, title):
        super().__init__(title)
        self.setDisabled(False)


class Shortcut(QShortcut):
    def __init__(self, key_sequence, widget, slot):
        super().__init__(key_sequence, widget, slot)


class Slider(QSlider):
    def __init__(self):
        super().__init__()


class SpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignRight)


class StandardPaths(QStandardPaths):
    def __init__(self):
        super().__init__()


class TextEdit(QTextEdit):
    def __init__(self):
        super().__init__()


class Thread(QThread):
    def __int__(self):
        super().__init__()


class TreeView(QTreeView):
    def __init__(self):
        super().__init__()
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)


class VBoxLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
