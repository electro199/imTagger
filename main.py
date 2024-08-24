import json
from pathlib import Path
import sys
from typing import Any
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QKeySequence, QPixmap, QIcon, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QDialog,
    QMenu,
)

from PySide6.QtGui import QImageReader, QPixmap, QShortcut, QClipboard
from PySide6.QtCore import Qt
from ui.app_ui import Ui_MainWindow
from ui.custom_input_iu import InputDialog
from glob import glob
import csv
import logging

Auto_Labbeler_ENABLED = False

if Auto_Labbeler_ENABLED:
    from auto_labeler import Auto_Labbeler
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("icons/empty-icon copy.jpg"))
        self.current_image: str = ""
        self.all_images_path: list[str] = []
        self.all_labels: list[str | None] = []

        self.all_unique_labels: list[str | None] = []

        self.__current_image_index = -1

        self.labels_count = -1
        self._defaults = {}
        self.is_dataset_changed: bool = False
        self.progress_file_path: str | None = ""
        self.save_defaults()

        self.ui.label_holder.setWidgetResizable(True)

        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(2000)

        self.ui.image_area.setContextMenuPolicy(Qt.CustomContextMenu)  # type: ignore
        self.ui.image_area.customContextMenuRequested.connect(self.show_context_menu)

        self.ui.actionopen_folder.triggered.connect(self.open_folder)
        self.ui.actionOpen_img_csv.triggered.connect(self.open_img_csv)
        self.ui.actionOpen_Labels_file.triggered.connect(self.get_labels)
        
        self.ui.actionSave_project.triggered.connect(self.savedataset)
        self.ui.actionsave_progress.triggered.connect(self.save_progress_file)
        self.ui.actionload_from_progress_file.triggered.connect(
            self.load_from_progress_file
        )
        self.ui.add_Label.pressed.connect(self._add_label_manual)

        shortcut_a = QShortcut(QKeySequence(Qt.Key_A), self)  # type: ignore
        shortcut_a.activated.connect(self.on_a_key_pressed)

        shortcut_d = QShortcut(QKeySequence(Qt.Key_D), self)  # type: ignore
        shortcut_d.activated.connect(self.on_d_key_pressed)
        if Auto_Labbeler_ENABLED:
            self.model = Auto_Labbeler()
            self.model.result_signal.connect(self.set_label)


    @Slot(str)
    def set_label(self,text):
        if not text:
            self.ui.current_image_path_label.setText("No Label")
            if Auto_Labbeler_ENABLED:
                self.model.set_image_path(self.current_image)
                self.model.start()
            return

        self.ui.current_image_path_label.setText(text)

    @property
    def current_image_index(self) -> int:
        return self.__current_image_index

    @current_image_index.setter
    def current_image_index(self, num) -> None:
        self.__current_image_index = num
        self.ui.progressBar.setValue(num + 1)
        self.ui.progressBar.setMaximum(len(self.all_images_path))

    def show_context_menu(self, position) -> None:
        context_menu = QMenu(self)

        # Create actions
        copy_image_path_action = QAction("Copy Image Path", self)
        # action_2 = QAction("Copy Image Label", self)

        copy_image_path_action.triggered.connect(
            lambda: QClipboard(self).setText(self.current_image)
        )
        # action_2.triggered.connect(lambda: QClipboard(self).setText(self.))

        context_menu.addAction(copy_image_path_action)
        # context_menu.addAction(action_2)

        context_menu.exec(self.mapToGlobal(position))

    def _add_label_manual(self) -> None:
        self._add_label(self.labels_count + 1, self.open_input_dialog())

    def open_folder(self) -> None:
        file_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.to_defaults()
        self.set_labels_disabled(False)

        logging.info("Loading from folder : ", file_path)
        self.all_images_path = (
            glob(file_path + "/**/**.png")
            + glob(file_path + "/**/**.jpg")
            + glob(file_path + "/**.jpg")
            + glob(file_path + "/**.png")
        )
        self.all_labels.extend([None] * len(self.all_images_path))
        logging.info(self.all_images_path)
        self.show_next_image()
        return

    def open_img_csv(self) -> None:
        file_path, _ = QFileDialog.getOpenFileUrl(self, "Select image csv", ".")

        if not file_path:
            return

        self.to_defaults()

        with open(str(file_path.toLocalFile()), encoding="utf-8") as f:

            self.all_images_path = [i["path"] for i in csv.DictReader(f)]

        self.show_next_image()

    def get_labels(self) -> None:
        file_path, _ = QFileDialog.getOpenFileUrl(self, "Select Label file", ".")
        with open(str(file_path.toLocalFile())) as f:
            self.add_labels(f.read().strip().split("\n"))

    def show_next_image(self,) -> None:

        if (self.current_image_index + 1) > (len(self.all_images_path) - 1):
            image_reader = QImageReader(
                str(Path(__file__).parent.joinpath("icons", "empty-icon.jpg"))
            )
            return
        
        self.current_image_index += 1

        self.current_image = self.all_images_path[self.current_image_index]
        image_reader = QImageReader(self.current_image)
        # try:
        
        self.set_label(self.all_labels[self.current_image_index])
        
        logging.debug(self.current_image)

        pixmap = QPixmap.fromImageReader(image_reader)

        if pixmap.isNull():
            logging.info("found broken image", self.current_image)
            pixmap = QPixmap.fromImageReader(QImageReader("icons/broken-image.png"))
            return self.display_image(pixmap)

        self.display_image(pixmap)

    def show_previous_image(self) -> None:

        if self.current_image_index - 1 < 0:
            return
        
        self.current_image_index -= 1
        
        self.current_image = self.all_images_path[self.current_image_index]
        image_reader = QImageReader(self.current_image)

        self.set_label(self.all_labels[self.current_image_index])            

        pixmap = QPixmap.fromImageReader(image_reader)

        if pixmap.isNull():
            logging.info("found broken image", self.current_image)
            pixmap = QPixmap.fromImageReader(QImageReader("icons/broken-image.png"))
            return self.display_image(pixmap)

        self.display_image(pixmap)

    def display_image(self, pixmap: QPixmap) -> None:
        self.ui.image_area.setPixmap(
            pixmap.scaled(
                self.ui.image_area.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation  # type: ignore
            )
        )

    def add_labels(self, label_list) -> None:
        self.set_labels_disabled(False)

        for i, label in enumerate(label_list):
            self._add_label(i, label)
        self.labels_count = i
        self.ui.verticalLayout_2.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # type: ignore
        )

    def _add_label(self, i, label) -> None:
        if label is None:
            return
        if label in self.all_unique_labels:
            logging.info(label, "already in labels skipping...")
            return

        self.labels_count += 1

        button = QPushButton(f"{self.labels_count + 1}. {label}", self)
        button.setObjectName(label)
        button.clicked.connect(self.on_button_clicked)
        button.setShortcut(QKeySequence(f"Ctrl+{i + 1}"))

        logging.info("Adding label : ", self.labels_count)
        self.ui.verticalLayout_2.insertWidget(i, button)
        self.all_unique_labels.append(label)

    def clear_label_holder(self):
        while self.ui.verticalLayout_2.count() > 1:
            item = self.ui.verticalLayout_2.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def open_input_dialog(self) -> str | None:
        dialog = InputDialog()
        if dialog.exec() == QDialog.Accepted:  # type: ignore #
            input_text = dialog.get_input_text()
            logging.info(f"Input text: {input_text}")
            return input_text

    def on_button_clicked(self) -> None:
        label = self.sender().objectName()
        logging.info(f"Button with label '{label}' clicked!")
        # TODO do somthing...
        # self.label2img[label].append(self.current_image)
        self.all_labels[self.current_image_index] = label
        self.is_dataset_changed = True

        self.show_next_image()

    def set_labels_disabled(self, bool_arg) -> None:
        self.ui.label_holder.setDisabled(bool_arg)

    def resizeEvent(self, event) -> None:
        print("1")
        if self.ui.image_area.pixmap():
            print("2")
            self.display_image(
                QPixmap.fromImageReader(
                    QImageReader(self.all_images_path[self.current_image_index])
                )
            )
        super().resizeEvent(event)

    def savedataset(self) -> None:
        "Open dialog to get file info and extension is the imtag"

        file_path, _ = QFileDialog.getSaveFileName(
            self, caption="Save  Dataset", filter="*.csv"
        )

        if not file_path:  # Check if a file path was selected
            logging.error("empty file path detected for savedataset NOT SAVING ")
            return
        # Ensure the file has the correct extension
        if not file_path.endswith(".csv"):
            file_path += ".csv"

        logging.info("Saving to ", file_path)

        self.progress_file_path = file_path

        with open("dataset.csv", "w", encoding="utf-8") as f:
            w = csv.DictWriter(f, {"label", "path"}, lineterminator="\n")
            w.writeheader()
            b = []
            # for key in self.label2img:
            #     for v in self.label2img[key]:
            #         b.append({"label": key, "path": v})
            for key, v in zip(self.all_labels, self.all_images_path):
                b.append({"label": key, "path": v})
            w.writerows(b)

    def save_defaults(self) -> None:
        """
        Saves the internal state to data holder
        """
        self._defaults["current_image"] = self.current_image
        self._defaults["all_images_path"] = self.all_images_path
        self._defaults["current_image_index"] = self.current_image_index
        self._defaults["labels_count"] = self.labels_count
        self._defaults["all_labels"] = self.all_labels
        self._defaults["all_unique_labels"] = self.all_unique_labels

    def to_defaults(self) -> None:
        """
        Resets App state and clear the clear the label holders
        """
        self.current_image = self._defaults["current_image"]
        self.all_images_path = self._defaults["all_images_path"]
        self.current_image_index = self._defaults["current_image_index"]
        self.labels_count = self._defaults["labels_count"]
        self.all_labels = self._defaults["all_labels"]
        self.all_unique_labels = self._defaults["all_unique_labels"]
        self.clear_label_holder()

    def save_progress_file(self) -> None:

        if not self.progress_file_path:
            self.progress_file_path, _ = QFileDialog.getSaveFileName(
                self,
                caption="Save Progress File",
                dir="/progress.json",
                filter="imtag files (*.imtag)",
            )

            if not self.progress_file_path:
                logging.info("empty file path detected for save progress NOT SAVING ")
                return

        app_state = {
            "current_image": self.current_image,
            "all_images_path": self.all_images_path,
            "all_labels": self.all_labels,
            "current_image_index": self.current_image_index,
            # "label2img": self.label2img,
            "labels_count": self.labels_count,
            "v": "0.0.1",
        }
        with open(self.progress_file_path, "w", -1, "utf-8") as f:
            json.dump(app_state, f, indent=2)

    def load_from_progress_file(self) -> None:
        dir, _ = QFileDialog.getOpenFileUrl(self, filter="IMTAG files (*.imtag)")
        self.progress_file_path = dir.toLocalFile()
        if not self.progress_file_path:
            return

        with open(self.progress_file_path, "r", -1, "utf-8") as f:
            app_state: dict[str, Any] = json.load(f)

        self.to_defaults()

        self.current_image = app_state["current_image"]
        self.current_image_index = app_state["current_image_index"]
        self.all_images_path = app_state["all_images_path"]

        label2img = app_state.get("label2img")

        if label2img:
            for path in self.all_images_path:
                label_found = None
                # Search for the label that contains the current path
                for label, paths in label2img.items():
                    if path in paths:
                        label_found = label
                        break
                # Append the found label (or None if not found) to the output list
                self.all_labels.append(label_found)
            self.add_labels(label2img.keys())
        else:
            self.all_labels = app_state["all_labels"]
            self.add_labels(
                {label for label in app_state["all_labels"] if label is not None}
            )

        # Assert that both lists have the same length
        assert len(self.all_images_path) == len(
            self.all_labels
        ), f"Lengths of image_paths and image_labels {len(self.all_images_path)=}{len(self.all_labels)=} {self.all_images_path=}{self.all_labels=}"

        assert (
            self.labels_count == app_state["labels_count"]
        ), "SOME thing broke with label file for holder"

        # if len(self.all_relative_image) > len(self.all_labels):
        #     self.all_labels.extend([None] * len(self.all_relative_image))

        logging.debug(self.all_images_path)
        logging.debug("=" * 20)
        logging.debug(self.all_labels)
        self.display_image(QPixmap.fromImageReader(QImageReader(self.current_image)))
        self.ui.current_image_path_label.setText(
            self.all_labels[self.current_image_index]
        )

    def autosave(self):
        if not (self.is_dataset_changed and self.progress_file_path):
            logging.debug(
                "skipping autosave", self.is_dataset_changed, self.progress_file_path
            )
            return

        logging.info("autosaving", self.is_dataset_changed, self.progress_file_path)
        self.save_progress_file()

    def on_a_key_pressed(self):
        self.show_previous_image()

    def on_d_key_pressed(self):
        self.show_next_image()

    def on_closing(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
