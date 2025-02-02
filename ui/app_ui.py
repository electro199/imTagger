# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionopen_folder = QAction(MainWindow)
        self.actionopen_folder.setObjectName(u"actionopen_folder")
        self.actionOpen_Labels_file = QAction(MainWindow)
        self.actionOpen_Labels_file.setObjectName(u"actionOpen_Labels_file")
        self.actionSave_project = QAction(MainWindow)
        self.actionSave_project.setObjectName(u"actionSave_project")
        self.actionOpen_img_csv = QAction(MainWindow)
        self.actionOpen_img_csv.setObjectName(u"actionOpen_img_csv")
        self.actionsave_dataset = QAction(MainWindow)
        self.actionsave_dataset.setObjectName(u"actionsave_dataset")
        self.actionload_from_progress_file = QAction(MainWindow)
        self.actionload_from_progress_file.setObjectName(u"actionload_from_progress_file")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_holder = QScrollArea(self.widget)
        self.label_holder.setObjectName(u"label_holder")
        self.label_holder.setWidgetResizable(True)
        self.label_holder.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 198, 523))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label_holder.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.label_holder)

        self.add_Label = QPushButton(self.widget)
        self.add_Label.setObjectName(u"add_Label")

        self.verticalLayout.addWidget(self.add_Label)

        self.current_image_path_label = QLabel(self.widget)
        self.current_image_path_label.setObjectName(u"current_image_path_label")
        self.current_image_path_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.current_image_path_label)


        self.horizontalLayout.addWidget(self.widget)

        self.image_area = QLabel(self.centralwidget)
        self.image_area.setObjectName(u"image_area")
        self.image_area.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.image_area)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionopen_folder)
        self.menuFile.addAction(self.actionOpen_img_csv)
        self.menuFile.addAction(self.actionOpen_Labels_file)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_project)
        self.menuFile.addAction(self.actionsave_dataset)
        self.menuFile.addAction(self.actionload_from_progress_file)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionopen_folder.setText(QCoreApplication.translate("MainWindow", u"Open folder", None))
        self.actionOpen_Labels_file.setText(QCoreApplication.translate("MainWindow", u"Open Labels file", None))
        self.actionSave_project.setText(QCoreApplication.translate("MainWindow", u"Save dataset", None))
        self.actionOpen_img_csv.setText(QCoreApplication.translate("MainWindow", u"Open img csv", None))
        self.actionsave_dataset.setText(QCoreApplication.translate("MainWindow", u"save_progress", None))
        self.actionload_from_progress_file.setText(QCoreApplication.translate("MainWindow", u"load from progress file", None))
        self.add_Label.setText(QCoreApplication.translate("MainWindow", u"Add Label", None))
        self.current_image_path_label.setText(QCoreApplication.translate("MainWindow", u"current image", None))
        self.image_area.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

