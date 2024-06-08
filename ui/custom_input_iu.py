from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
)


class InputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Input Dialog")

        # Create layout
        layout = QVBoxLayout()

        # Create label
        self.label = QLabel("Enter your text:")
        layout.addWidget(self.label)

        # Create text input
        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        # Create button
        self.button = QPushButton("OK")
        layout.addWidget(self.button)

        # Connect button click signal to the slot
        self.button.clicked.connect(self.on_button_clicked)

        # Set the layout
        self.setLayout(layout)

    def on_button_clicked(self):
        # Retrieve the text from the input
        self.input_text = self.text_input.text()

        # Close the dialog
        self.accept()

    def get_input_text(self):
        return self.input_text
