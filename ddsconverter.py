from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QFileDialog, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QStatusBar, QApplication, QComboBox, QHBoxLayout
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtCore import QUrl, QSize, QProcess, QDir
import settings
from settings import DDSTextureFormat, AlphaMethod, Preset

#https://python-forum.io/thread-43484.html subprocessing

class DDSConverter(QWidget):
    def __init__(self,status_bar):
        super().__init__()
        self.convert_list = []
        self.out_put_dir = QDir.currentPath() + "/Converted"
        self.power_of_two = True
        self.mip_level = "0"
        self.compression_format = settings.DDSTextureFormat.BC3_UNORM.name
        self.alpha_method = "-pmalpha"

        self.grid_layout = QGridLayout()
        self.list_widget = QListWidget()

        self.parent_status_bar = status_bar
        self.file_path_le = QLineEdit("")
        self.file_path_button = QPushButton("Add Images")
        self.convert_button = QPushButton("Convert")

        #Settings
        self.preset_setting_label = QLabel("Preset")
        self.preset_setting = QComboBox()
        self.compression_setting_label = QLabel("Format")
        self.compression_setting = QComboBox()
        self.alpha_settings_label = QLabel("Alpha")
        self.alpha_setting = QComboBox()
        self.out_put_dir_label = QLabel("Output Directory")
        self.out_put_dir_le = QLineEdit()
        self.output_dir_button = QPushButton("Directory")

        self.image_label = QLabel("Image")
        self.current_image = QPixmap(QSize(550,550))
        self.current_image = self.current_image.scaled(550, 550, aspectMode=Qt.AspectRatioMode.KeepAspectRatio)

        self.init_ui()

        self.connect_signals()

    def init_ui(self):

        self.preset_setting_label.setBuddy(self.preset_setting)
        self.compression_setting_label.setBuddy(self.compression_setting)
        self.alpha_settings_label.setBuddy(self.alpha_setting)
        self.out_put_dir_label.setBuddy(self.out_put_dir_le)

        preset_settings = QHBoxLayout()
        preset_settings.addWidget(self.preset_setting_label)
        preset_settings.addWidget(self.preset_setting)

        format_settings = QHBoxLayout()
        format_settings.addWidget(self.compression_setting_label)
        format_settings.addWidget(self.compression_setting)
        self.compression_setting.setCurrentIndex(settings.DDSTextureFormat.BC3_UNORM.value) #FIX THIS TO TAKE FROM PARAM

        alpha_settings = QHBoxLayout()
        alpha_settings.addWidget(self.alpha_settings_label)
        alpha_settings.addWidget(self.alpha_setting)

        out_put_dir_layout = QHBoxLayout()
        out_put_dir_layout.addWidget(self.out_put_dir_label)
        out_put_dir_layout.addWidget(self.out_put_dir_le)
        out_put_dir_layout.addWidget(self.output_dir_button)

        self.file_path_le.setDisabled(True)
        self.out_put_dir_le.setDisabled(True)

        #Init default text field
        self.out_put_dir_le.setText(self.out_put_dir)

        self.image_label.setMaximumWidth(550)
        self.image_label.setMaximumHeight(550)

        self.image_label.setPixmap(self.current_image)

        self.grid_layout.addWidget(self.image_label,0,0)
        self.grid_layout.addWidget(self.file_path_le,1,0)
        self.grid_layout.addWidget(self.file_path_button,6,1)
        self.grid_layout.addWidget(self.list_widget,0,1,6,1)
        #self.grid_layout.addWidget(self.compression_setting_label,3,0)
        #self.grid_layout.addWidget(self.compression_setting,3,1)
        self.grid_layout.addLayout(preset_settings,3,0)
        self.grid_layout.addLayout(format_settings,4,0)
        self.grid_layout.addLayout(alpha_settings,5,0)
        self.grid_layout.addLayout(out_put_dir_layout,6,0)
        self.grid_layout.addWidget(self.convert_button,7,0,1,2)

        self.convert_button.setMinimumHeight(75)

        self.setLayout(self.grid_layout)

        self.populate_settings_options()

        #Start Exceptions
        self.preset_setting_changed()
        self.parent_status_bar.showMessage("") #prevent run at start

    def populate_settings_options(self):
        for setting in Preset:
            self.preset_setting.addItem(setting.name)
        for setting in DDSTextureFormat:
            self.compression_setting.addItem(setting.name)
        for setting in AlphaMethod:
            self.alpha_setting.addItem(setting.name)

    def connect_signals(self):
        self.file_path_button.clicked.connect(self.set_file_path)
        self.list_widget.itemClicked.connect(self.set_active_file)
        self.convert_button.clicked.connect(self.convert_to_dds)
        self.preset_setting.currentIndexChanged.connect(self.preset_setting_changed)
        self.compression_setting.currentIndexChanged.connect(self.compression_setting_changed)
        self.alpha_setting.currentIndexChanged.connect(self.alpha_setting_changed)
        self.output_dir_button.clicked.connect(self.set_output_dir)

    def set_output_dir(self):
        selected_folder = QFileDialog().getExistingDirectoryUrl()
        if selected_folder == "": #maybe fix
            return
        self.out_put_dir_le.setText(selected_folder.toLocalFile())
        self.out_put_dir = selected_folder.toLocalFile()

    def preset_setting_changed(self):
        if self.preset_setting.currentText() == Preset.ALBEDO.name:
            self.compression_setting.setCurrentIndex(DDSTextureFormat.BC7_UNORM_SRGB.value)
        elif self.preset_setting.currentText() == Preset.NORMAL.name:
            self.compression_setting.setCurrentIndex(DDSTextureFormat.BC5_UNORM.value)
        elif self.preset_setting.currentText() == Preset.MATERIAL.name:
            self.compression_setting.setCurrentIndex(DDSTextureFormat.BC7_UNORM.value)
        elif self.preset_setting.currentText() == Preset.FX.name:
            self.compression_setting.setCurrentIndex(DDSTextureFormat.BC3_UNORM.value)

        self.parent_status_bar.showMessage(f"Preset Changed to {self.preset_setting.currentText()}")

    def compression_setting_changed(self):
        self.compression_format = self.compression_setting.currentText()
        self.parent_status_bar.showMessage(f"Setting Changed to: {self.compression_format}")

    def alpha_setting_changed(self):
        if self.alpha_setting.currentText() == AlphaMethod.PREMULTIPLIED.name:
            self.alpha_method = AlphaMethod.PREMULTIPLIED.value
        elif self.alpha_setting.currentText() == AlphaMethod.STRAIGHT.name:
            self.alpha_method = AlphaMethod.STRAIGHT.value
        elif self.alpha_setting.currentText() == AlphaMethod.SEPERATE.name:
            self.alpha_method = AlphaMethod.SEPERATE.value

        self.parent_status_bar.showMessage(f"Alpha Settings Changed to {self.alpha_setting.currentText()}")

    def set_active_file(self):
        self.file_path_le.setText(self.list_widget.currentItem().text())
        self.set_active_image()

    def set_active_image(self):
        self.current_image = QPixmap(self.file_path_le.text())
        self.current_image = self.current_image.scaled(550, 550, aspectMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(self.current_image)

    def set_file_path(self):
        file_dialog = QFileDialog.getOpenFileUrls(self,"Input Image","","Images (*.png *.jpg *.jpeg *.tga)")
        success = file_dialog[1]
        if success:
            self.convert_list = []
            for file in file_dialog[0]:
                file_path = file.toLocalFile()
                item = QListWidgetItem()
                item.setText(file_path)
                self.list_widget.addItem(item)
                self.file_path_le.setText(file_path)
                self.set_active_image()
                self.convert_list.append(file_path)

    def convert_to_dds(self):
        if len(self.convert_list)==0:
            self.parent_status_bar.showMessage("No Images to Convert")
            return

        for index, image in enumerate(self.convert_list):
            command = [
                '-f',self.compression_format, #Compression
                '-m',self.mip_level, #Mip maps
                '-o',self.out_put_dir, #Output Dir
                self.alpha_method,
                '-y',  # Overwrite y/n
                image #input image file path
            ]

            if self.power_of_two:
                command.append('-pow2')

            process = QProcess(self)
            process.start("texconv.exe",command)
            process.waitForStarted()
            process.waitForFinished()

            self.parent_status_bar.showMessage(f"Converted {index + 1} / {len(self.convert_list)} Images to DDS")

            QApplication.instance().processEvents()

        self.parent_status_bar.showMessage(f"{len(self.convert_list)} Images Converted to DDS")