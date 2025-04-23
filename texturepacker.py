from PIL.Image import Dither
from PySide6.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit,QPushButton,
                               QHBoxLayout, QVBoxLayout, QFileDialog)
from PySide6.QtGui import QPixmap, Qt, QColor
from PySide6.QtCore import QSize,Signal, QUrl
from PIL import Image, ImageChops, ImageFilter


class TexturePacker(QWidget):

    def __init__(self):
        super().__init__()
        self.r_image = ImageInput(128,128,"Red Channel")
        self.g_image = ImageInput(128,128, "Green Channel")
        self.b_image = ImageInput(128,128,"Blue Channel")
        self.a_image = ImageInput(128,128,"Alpha Channel")
        self.output_image = ImageInput(512,512, "Output Image")

        self.pack_button = QPushButton("Pack Texture")

        self.grid_layout = QGridLayout()

        self.init_ui()

    def init_ui(self):

        self.grid_layout.addLayout(self.r_image.layout,0,0)
        self.grid_layout.addLayout(self.g_image.layout,0,1)
        self.grid_layout.addLayout(self.b_image.layout,0,2)
        self.grid_layout.addLayout(self.a_image.layout,0,3)
        self.grid_layout.addLayout(self.output_image.layout,1,0,1,4)
        self.grid_layout.addWidget(self.pack_button,2,1,1,2)
        self.setLayout(self.grid_layout)

        self.output_image.toggle_enable_button()

        self.pack_button.pressed.connect(self.merge_images)

    def merge_images(self):
        print(self.r_image.image_path)
        r = save_image(self.r_image.image_path)
        b = save_image(self.g_image.image_path)
        g = save_image(self.b_image.image_path)
        a = save_image(self.a_image.image_path)
        new_image = Image.merge("RGBA",(r,g,b,a))
        new_image.save("temp.png")
        #new_image.show() #Testing
        self.output_image.set_pixmap("temp.png")

#better name? FIX
def save_image(path):
    image = Image.open(path)
    print(image.mode)
    image = image.convert('RGB')
    image = image.convert('L')

    #image = image.resize((550,550),Image.Resampling.LANCZOS)
    #new_img_path = "" + QUrl(path).fileName()
    #image.save(new_img_path,'png')
    return image# Return first channel since all channels are the same value

class ImageInput:

    #image_changed = Signal(str)

    def __init__(self, width, height, title):
        self.image_path = ""
        self.width = width
        self.height = height

        self.layout = QGridLayout()

        self.pixmap = QPixmap(QSize(height,width))
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label = QLabel()
        self.file_button = QPushButton("File")

        self.container = QWidget()
        self.container.setMaximumWidth(width)

        v_layout = QVBoxLayout()
        #v_layout.addWidget(self.image_le)
        v_layout.addWidget(self.file_button)
        #v_layout.setStretch(0,4)
        #v_layout.setStretch(1,1)

        self.container.setLayout(v_layout)

        self.layout.addWidget(self.title_label,0,0)
        self.layout.addWidget(self.image_label, 1, 0)
        self.layout.addWidget(self.container,2,0)

        self.set_pixmap("")

        self.file_button.pressed.connect(self.load_image)


    def set_pixmap(self,path):
        self.image_label.setFixedSize(QSize(self.width, self.height))
        if path == "":
            self.pixmap = QPixmap(self.width,self.height)
            self.pixmap.fill(QColor("black"))
        else:
            self.pixmap = QPixmap(path)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setScaledContents(True)


    def load_image(self):
        path = QFileDialog.getOpenFileUrl(self.container,"Input Image","","Images (*.png *.jpg *.jpeg *.tga)")
        success = path[0]
        if success:
            self.set_pixmap(path[0].toLocalFile())
            self.image_path=path[0].toLocalFile()
            #self.image_changed.emit(title)

    def toggle_enable_button(self):
        self.file_button.setEnabled(not self.file_button.isEnabled())
        self.file_button.setHidden(not self.file_button.isHidden())