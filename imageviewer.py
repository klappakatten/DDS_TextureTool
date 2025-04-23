from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize
from PIL import Image



class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.image_file_path = ""

        self.grid_layout = QGridLayout()

        self.file_button = QPushButton("File")
        self.r_button = QPushButton("R")
        self.g_button = QPushButton("G")
        self.b_button = QPushButton("B")
        self.a_button = QPushButton("A")

        self.image_label = QLabel()
        self.file_le = QLineEdit()

        self.init_ui()

        self.connect_signals()

    def init_ui(self):
        self.image_label.setPixmap(QPixmap(QSize(1024,1024)))
        self.image_label.setScaledContents(True)
        self.file_le.setEnabled(False)

        self.grid_layout.addWidget(self.r_button,0,0)
        self.grid_layout.addWidget(self.g_button,0,1)
        self.grid_layout.addWidget(self.b_button,0,2)
        self.grid_layout.addWidget(self.a_button,0,3)
        self.grid_layout.addWidget(self.image_label,1,0,1,4)
        self.grid_layout.addWidget(self.file_le,2,0,1,4)
        self.grid_layout.addWidget(self.file_button,3,0,1,4)
        self.setLayout(self.grid_layout)

    def connect_signals(self):
        self.file_button.clicked.connect(self.get_file_path)
        self.r_button.clicked.connect(self.show_channel)
        self.g_button.clicked.connect(self.show_channel)
        self.b_button.clicked.connect(self.show_channel)
        self.a_button.clicked.connect(self.show_channel)

    def show_channel(self):
        button = self.sender()

        image = Image.open(self.image_file_path).convert('RGBA')
        r,g,b,a = image.split()

        if button == self.r_button:
            r.save("temp.png")
        elif button == self.g_button:
            g.save("temp.png")
        elif button == self.b_button:
            b.save("temp.png")
        elif button == self.a_button:
            a.save("temp.png")

        self.image_label.setPixmap(QPixmap("temp.png"))

    def get_file_path(self):
        path = QFileDialog.getOpenFileUrl(self.file_button, "Input Image", "", "Images (*.png *.jpg *.jpeg *.tga)")
        success = path[0]
        if success:
            self.file_le.setText(success.toLocalFile())
            self.image_file_path = success.toLocalFile()
            self.set_pixmap()

    def set_pixmap(self):
        pixmap = QPixmap(self.image_file_path)
        self.image_label.setPixmap(pixmap)