from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QLineEdit,
    QApplication,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PIL import Image
from PIL.ImageQt import ImageQt
import os

from quiz.view.process_image import Ui_Dialog
from quiz.prepstuff.getQuestions import FreelancerQuizOcr


class QuizProcessingDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.ocr_processor = FreelancerQuizOcr()
        self.current_question = None
        self.current_answers = []
        self.current_image_index = -1
        self.images = []
        self.answer_edits = []

        # Connect buttons
        self.process_directory_pb.clicked.connect(self.select_directory)
        self.next_btn.clicked.connect(self.load_next_image)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.process_directory_le.setText(directory)
            self.load_directory(directory)

    def load_directory(self, directory):
        self.images = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        self.current_image_index = -1
        self.load_next_image()

    def display_image(self, file_path):
        # Open as a QPixmap
        img = QPixmap(file_path)
        # Scale to fit the label
        img = img.scaled(self.image_label.size(), Qt.KeepAspectRatio)

        self.image_label.setPixmap(img)

    def load_next_image(self):
        self.clear_form()
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            current_image_path = self.images[self.current_image_index]
            self.display_image(current_image_path)
            self.ocr_processor.process_file(current_image_path)

    def clear_form(self):
        self.image_label.clear()
        self.question_edit.clear()
        for ans_edit in self.answer_edits:
            ans_edit.clear()


# Example usage
if __name__ == "__main__":
    app = QApplication([])
    dialog = QuizProcessingDialog()
    dialog.show()
    app.exec()
