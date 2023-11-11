from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
)


class LoadCsvYesNo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Load Questions from csv")
        self.setup_ui()
        self.user_choice = None
        self.do_not_ask_again = False

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Dialog message
        msg = self.create_message()
        self.label = QLabel(msg)
        self.label.setStyleSheet(
            """
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.987, y2:0.579545, stop:0.028065 rgba(30, 82, 139, 255), stop:0.731343 rgba(12, 34, 89, 255));
            }
            ul {
                margin-left: 20px;
                list-style: none;
                list-style: none;
            }
            li {
                margin: 5px 0;
                color: #ffffff;
            }
            """
        )

        layout.addWidget(self.label)

        # Checkbox
        self.checkbox = QCheckBox("Do not ask again. Just load the questions.")
        layout.addWidget(self.checkbox)

        # Yes/No buttons
        button_layout = QHBoxLayout()
        self.yes_button = QPushButton("Yes")
        self.no_button = QPushButton("No")
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)
        layout.addLayout(button_layout)

        # Connect signals
        self.yes_button.clicked.connect(self.accept)
        self.no_button.clicked.connect(self.reject)
        self.checkbox.stateChanged.connect(self.checkbox_changed)

    def create_message(self):
        # Your HTML message
        msg = (
            "<html>"
            "<head/>"
            "<body>"
            '<p><span style="font-size:22pt; font-weight:700; color:#deddda;">Load Questions from CSV</span></p>'
            '<span style="color:#ffffff;">'
            "<p>This action will load a list of questions from a CSV file. The CSV file should be formatted as follows:</p>"
            '<p style="margin-left: 20px;"><b>Format:</b> [question, answer1, answer2, answer3, answer4, ...]</p>'
            "<ul>"
            "<li>You may optionally include a <b>correct_answer</b> column.</li>"
            "<li>You may also include a <b>notes</b> column for additional context.</li>"
            "<li>The GPT explanation can assist in setting the correct answer later, if needed.</li>"
            "</ul>"
            '<p><span style="font-size:18pt; font-weight:700; color:#deddda;">Do you want to load the CSV file?</span></p>'
            "</span>"
            "</body>"
            "</html>"
        )
        return msg

    def checkbox_changed(self, state):
        self.do_not_ask_again = state == 2

    def accept(self):
        self.user_choice = True
        super().accept()

    def reject(self):
        self.user_choice = False
        super().reject()


# Example usage
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dialog = LoadCsvYesNo()
    dialog.exec()

    if dialog.user_choice:
        print("User chose Yes.")
    else:
        print("User chose No.")

    if dialog.do_not_ask_again:
        print("User chose not to be asked again.")
