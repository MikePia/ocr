from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpacerItem,
    QVBoxLayout,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

import os
from quiz.models.Question import Answer, Question

from quiz.view.process_image import Ui_Dialog
from quiz.prepstuff.getQuestions import FreelancerQuizOcr
from quiz.models.utils.finddup import find_duplicates


class QuizProcessingDialog(QDialog, Ui_Dialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setupUi(self)
        self.ocr_processor = FreelancerQuizOcr()
        self.current_question = None
        self.current_answers = []
        self.current_image_index = -1
        self.images = []
        self.answer_edits = []
        self.raw_question = []
        self.answer_layout = None

        # Connect buttons
        self.process_directory_pb.clicked.connect(self.select_directory)
        self.process_image_pb.clicked.connect(self.process_image)
        self.next_btn.clicked.connect(self.load_next_image)
        self.add_answer_pb.clicked.connect(self.add_answer_widget)
        self.delete_answer_pb.clicked.connect(self.delete_answer_widget)
        self.save_btn.clicked.connect(self.save_question)
        self.close_btn.clicked.connect(self.close)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.process_directory_le.setText(directory)
            self.load_directory(directory)

    def process_image(self):
        # image = QFileDialog.getOpenFileName(self, "Open an image file")
        image, _ = QFileDialog.getOpenFileName(
            self,
            "Open an image file",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)",
        )
        if image:
            self.images = [image]
            self.current_image_index = -1
            self.load_next_image()

    def load_directory(self, directory):
        self.images = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        self.current_image_index = -1
        self.load_next_image()

    def display_image(self, file_path):
        img = QPixmap(file_path)
        img = img.scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(img)

    def load_next_image(self):
        """Load both the image and the question/answers"""
        self.clear_form()
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            current_image_path = self.images[self.current_image_index]
            self.display_image(current_image_path)
            self.ocr_processor.process_file(current_image_path)
            self.raw_question = self.ocr_processor.question
            self.question_edit.setText(self.raw_question[0])
            self.answer_edits = []

            # Clear existing layout
            if hasattr(self, "answer_layout") and self.answer_layout is not None:
                for i in reversed(range(self.answer_layout.count())):
                    widget = self.answer_layout.takeAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()

            for i, answer in enumerate(self.raw_question[1]):
                self.add_answer_widget(answer)
            self.answer_layout.addStretch(1)
        else:
            self.clear_form()

    def add_answer_widget(self, answer=None):
        # Ensure the layout is initialized
        if not hasattr(self, "answer_layout") or self.answer_layout is None:
            self.answer_layout = QVBoxLayout()
            self.answer_layout.setSpacing(0)  # Set spacing between widgets to 0
            self.answer_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
            self.answer_frame.setLayout(self.answer_layout)
            self.answer_layout.addStretch(1)  # Add stretch at the end of the layout

        # Create the answer QLineEdit
        answer_edit = QLineEdit(answer if answer else "")
        answer_edit.setStyleSheet(
            "background-color: rgb(255, 255, 255); color: rgb(36, 31, 49);"
        )
        self.answer_edits.append(answer_edit)

        # Insert the widget above the stretch
        self.answer_layout.insertWidget(self.answer_layout.count() - 1, answer_edit)

    def get_widget_to_remove(self):
        for i in reversed(range(self.answer_layout.count())):
            widget = self.answer_layout.itemAt(i).widget()
            if widget is not None and isinstance(widget, QLineEdit):
                return widget

    def delete_answer_widget(self):
        """Remove the last lineedit widget as seen on the screen. That will be the widget just before the stretch"""
        if self.answer_layout.count() > 1:
            # Get the widget at the second-to-last position (just before the stretch)
            widget_index = self.answer_layout.count() - 2
            # widget_to_remove = self.answer_layout.itemAt(widget_index).widget()
            widget_to_remove = self.get_widget_to_remove()

            if widget_to_remove:
                self.answer_layout.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)
                widget_to_remove.deleteLater()
                if widget_to_remove in self.answer_edits:
                    self.answer_edits.remove(widget_to_remove)

    def save_question(self):
        question = Question(
            question=self.question_edit.text(),
            answers=[Answer(answer=edit.text()) for edit in self.answer_edits],
        )

        dup = find_duplicates(self, self.user, question)
        if dup:
            formatquestion = (
                '<html><head/><body><p><span style="font-size:22pt; font-weight:700; color:#deddda;">'
                'Near Duplicates found </span></p><span style="color:#ffffff;"><p><b>Do you still want '
                f'to save this question? </b></p><hr><p class="question"> {dup.question}</p>'
            )
            for answer in dup.answers:
                formatquestion += f"<p>{answer.answer}</p>"
            formatquestion += "</span></body></html>"
            result = QMessageBox.question(
                self,
                "Near Duplicate found",
                formatquestion,
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            )
            if result == QMessageBox.Cancel or result == QMessageBox.No:
                self.load_next_image()
                return
        Question.store_question(question.question, [x.answer for x in question.answers])
        self.load_next_image()
        return

    def close(self) -> bool:
        return super().close()

    def clear_form(self):
        self.image_label.clear()
        self.question_edit.clear()
        self.raw_question = []

        # Clear answer edits
        while self.answer_edits:
            edit = self.answer_edits.pop()
            edit.deleteLater()
        if hasattr(self, "answer_layout") and self.answer_layout is not None:
            self.answer_layout.addStretch(1)


if __name__ == "__main__":

    class user:
        role = "admin"

    hack = user

    app = QApplication([])
    dialog = QuizProcessingDialog(hack)
    dialog.show()
    app.exec()
