from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QLabel, QWidget, QStatusBar, QTabWidget, QStackedWidget, QHBoxLayout
from PySide6.QtGui import QAction, QIcon, QImage, QKeySequence,Qt,QPalette,QColor
from ddsconverter import DDSConverter
from texturepacker import TexturePacker
from imageviewer import ImageViewer
import sys


#Icons https://p.yusukekamiyamane.com/, https://creativecommons.org/licenses/by/3.0/

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = QWidget()
        self.toolbar = QToolBar("Main Toolbar")
        self.statusbar = QStatusBar()

        self.page_layout = QHBoxLayout()
        self.stacked_layout = QStackedWidget()

        self.dds_panel = DDSConverter(self.statusbar)
        self.texture_packing_panel = TexturePacker()
        self.image_viewer_panel = ImageViewer()

        self.dds_action = QAction("Convert DDS", self)
        self.texture_pack_action = QAction("Texture Packing",self)
        self.image_preview_action = QAction("Image Viewer",self)
        self.actions = [self.dds_action, self.texture_pack_action, self.image_preview_action]

        self.init_ui()
        self.setup_actions()
        self.connect_signals()


    def init_ui(self):
        self.setWindowTitle("DDS Texture Tools")
        self.setCentralWidget(self.main_widget)

        self.main_widget.setMinimumWidth(500)
        self.main_widget.setMinimumHeight(500)

        self.stacked_layout.addWidget(self.dds_panel) ## Add DDS Panel
        self.stacked_layout.addWidget(self.texture_packing_panel) ## Add Texture Packing Panel
        self.stacked_layout.addWidget(self.image_viewer_panel) ## Add Image Preview Panel

        self.page_layout.addWidget(self.stacked_layout)
        self.main_widget.setLayout(self.page_layout)

        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.setStatusBar(self.statusbar)
        print("UI INITIATED")

    def connect_signals(self):
        self.dds_action.triggered.connect(lambda: self.button_toggled(0,self.dds_action))
        self.texture_pack_action.triggered.connect(lambda: self.button_toggled(1,self.texture_pack_action))
        self.image_preview_action.triggered.connect(lambda: self.button_toggled(2,self.image_preview_action))
        print("SIGNALS CONNECTED")

    def setup_actions(self):
        icon = QIcon("icons/image-export.png")
        self.dds_action.setIcon(icon)
        self.dds_action.setCheckable(True)
        self.dds_action.setChecked(True)

        icon = QIcon("icons/images-flickr.png")
        self.texture_pack_action.setIcon(icon)
        self.texture_pack_action.setCheckable(True)

        icon = QIcon("icons/image-empty.png")
        self.image_preview_action.setIcon(icon)
        self.image_preview_action.setCheckable(True)

        self.toolbar.addAction(self.dds_action)
        self.toolbar.addAction(self.texture_pack_action)
        self.toolbar.addAction(self.image_preview_action)

    def button_toggled(self,index, current_action):
        self.stacked_layout.setCurrentIndex(index)

        for action in self.actions:
            if current_action == action:
                action.setChecked(True)
            else:
                action.setChecked(False)

    def closeEvent(self, event, /):
        print("CLOSE EVENT FIRED!")
        #QSettings?


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()
    app.exec()

