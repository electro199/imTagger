import json
from pathlib import Path
import sys
from typing import Dict, List

from PySide6.QtCore import (
    Qt,
    QTimer
)
from PySide6.QtGui import QKeySequence, QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QDialog,
)

from PySide6.QtGui import QImageReader, QPixmap
from PySide6.QtCore import QDir, Qt
from ui.app_ui import Ui_MainWindow
from ui.custom_input_iu import InputDialog
from glob import glob
import csv


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(r"icons\empty-icon copy.jpg"))
        self.current_image = ""
        self.all_images_path = []
        self.current_image_index = -1
        self.label2img: Dict[str, List[str]] = {}
        self.labels_count = -1
        self._defaults = {}

        self.save_defaults()

        self.ui.label_holder.setWidgetResizable(True)

        self.ui.actionopen_folder.triggered.connect(self.open_folder)
        self.ui.actionOpen_Labels_file.triggered.connect(self.get_labels)
        self.ui.add_Label.pressed.connect(self._add_label_manual)
        self.ui.actionSave_project.triggered.connect(self.savedataset)
        self.ui.actionOpen_img_csv.triggered.connect(self.open_img_csv)
        self.ui.actionsave_dataset.triggered.connect(self.save_progress_file)
        self.ui.actionload_from_progress_file.triggered.connect(self.load_from_progress_file)


    def _add_label_manual(self) -> None:
        self._add_label(self.labels_count + 1, self.open_input_dialog())

    def open_folder(self) -> None:
        file_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.to_defaults()
        self.toggle_labels(False)

        print(file_path)
        self.all_images_path = (
            glob(file_path + "/**/**.png")
            + glob(file_path + "/**/**.jpg")
            + glob(file_path + "/**.jpg")
            + glob(file_path + "/**.png")
        )
        print(self.all_images_path)
        self.show_next_image()
        return

    def open_img_csv(self):
        file_path, _ = QFileDialog.getOpenFileUrl(self, "Select image csv", ".")
        with open(str(file_path.toLocalFile()), encoding="utf-8") as f:

            self.all_images_path = [i["path"] for i in csv.DictReader(f)]
        self.current_image_index = -1
        self.toggle_labels(False)
        self.show_next_image()

    def get_labels(self) -> None:
        file_path, _ = QFileDialog.getOpenFileUrl(self, "Select Label file", ".")
        with open(str(file_path.toLocalFile())) as f:
            self.add_labels(f.read().strip().split("\n"))

    def show_next_image(self) -> None:

        if (self.current_image_index + 1) > (len(self.all_images_path) - 1):
            image_reader = QImageReader(
                str(Path(__file__).parent.joinpath("icons", "empty-icon.jpg"))
            )
            self.toggle_labels(True)
            print(self.label2img)
        else:
            self.current_image = self.all_images_path[self.current_image_index + 1]
            self.ui.current_image_path_label.setText(self.current_image)
            image_reader = QImageReader(self.current_image)
        
        print(self.current_image)

        pixmap = QPixmap.fromImageReader(image_reader)
        if not pixmap.isNull():
            self.display_image(pixmap)
        self.current_image_index += 1

    def display_image(self, pixmap: QPixmap) -> None:
        self.ui.image_area.setPixmap(
            pixmap.scaled(
                self.ui.image_area.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def add_labels(self, label_list) -> None:
        self.toggle_labels(False)

        for i, label in enumerate(label_list):
            self._add_label(i, label)

        self.labels_count = i
        self.ui.verticalLayout_2.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def _add_label(self, i, label) -> None:
        if label in self.label2img:
            print(label, "already in labels skipping...")
            return

        self.labels_count += 1

        button = QPushButton(f"{self.labels_count + 1}. {label}", self)
        button.setObjectName(label)
        button.clicked.connect(self.on_button_clicked)
        button.setShortcut(QKeySequence(f"Ctrl+{i + 1}"))

        print(self.labels_count)
        self.ui.verticalLayout_2.insertWidget(i, button)
        self.label2img.update({label: []})

    def open_input_dialog(self):
        dialog = InputDialog()
        if dialog.exec() == QDialog.Accepted:
            input_text = dialog.get_input_text()
            print(f"Input text: {input_text}")
            return input_text

    def on_button_clicked(self):
        label = self.sender().objectName()
        print(f"Button with label '{label}' clicked!")
        # TODO do somthing...
        self.label2img[label].append(self.current_image)

        self.show_next_image()

    def toggle_labels(self, bool_arg):
        self.ui.label_holder.setDisabled(bool_arg)

    def resizeEvent(self, event):
        if self.ui.image_area.pixmap():
            self.display_image(self.ui.image_area.pixmap())
        super().resizeEvent(event)

    def savedataset(self):
        with open("dataset.csv", "w", encoding="utf-8") as f:
            w = csv.DictWriter(f, {"label", "path"}, lineterminator="\n")
            w.writeheader()
            b = []
            for key in self.label2img:
                for v in self.label2img[key]:
                    b.append({"label": key, "path": v})
            w.writerows(b)

    def save_defaults(self):
        self._defaults["current_image "] = self.current_image
        self._defaults["all_images_path "] = self.all_images_path
        self._defaults["current_image_index "] = self.current_image_index
        self._defaults["label2img "] = self.label2img
        self._defaults["labels_count "] = self.labels_count

    def to_defaults(self):
        self.current_image = self._defaults["current_image "]
        self.all_images_path = self._defaults["all_images_path "]
        self.current_image_index = self._defaults["current_image_index "]
        self.label2img = self._defaults["label2img "]
        self.labels_count = self._defaults["labels_count "]

    def save_progress_file(self):        
        app_state = {
        "current_image" : self.current_image,
        "all_images_path" : self.all_images_path,
        "current_image_index" : self.current_image_index,
        "label2img" : self.label2img,
        "labels_count" : self.labels_count,
    }
        with open("op.imtag", "w", -1, "utf-8") as f:
            json.dump(app_state, f, indent=2)

    def load_from_progress_file(self):
        dir ,_= QFileDialog.getOpenFileUrl(self)
        
        if not dir.toLocalFile():
            return 
        
        with open(dir.toLocalFile(), "r", -1, "utf-8") as f:
            app_state = json.load(f)

        self.current_image = app_state["current_image"]
        self.all_images_path = app_state["all_images_path"]
        self.current_image_index = app_state["current_image_index"]

        self.add_labels(app_state["label2img"].keys())
        self.label2img = app_state["label2img"]
        self.labels_count = app_state["labels_count"]
        
        self.display_image(QPixmap.fromImageReader(QImageReader(self.current_image)))

    def auto_save(self):
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
