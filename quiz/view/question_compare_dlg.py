from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QApplication,
)

from quiz.models.Question import Question, get_session


class QuestionComparisonDialog(QDialog):
    def __init__(self, question1, question2, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Compare Questions")
        self.setup_ui(question1, question2)

    def setup_ui(self, question1, question2):
        layout = QHBoxLayout(self)

        # Determine if questions are nearly equal
        nearly_equal = Question.nearly_equal(question1, question2)

        # Display for question 1
        question1_layout = QVBoxLayout()
        question1_layout.addWidget(QLabel(f"ID: {question1.id}"))
        question1_layout.addWidget(QLabel(f"Question: {question1.question}"))
        for answer in question1.answers:
            question1_layout.addWidget(QLabel(f"Answer: {answer.answer}"))
        layout.addLayout(question1_layout)

        # Display for question 2
        question2_layout = QVBoxLayout()
        question2_layout.addWidget(QLabel(f"ID: {question2.id}"))
        question2_layout.addWidget(QLabel(f"Question: {question2.question}"))
        for answer in question2.answers:
            question2_layout.addWidget(QLabel(f"Answer: {answer.answer}"))
        layout.addLayout(question2_layout)

        # Add a label to show comparison result
        comparison_result_label = QLabel(
            "Questions are nearly equal"
            if nearly_equal
            else "Questions are not nearly equal"
        )
        layout.addWidget(comparison_result_label)

        # Buttons
        buttons_layout = QVBoxLayout()
        delete_question1_button = QPushButton("Delete Question 1")
        delete_question2_button = QPushButton("Delete Question 2")
        cancel_button = QPushButton("Cancel")

        delete_question1_button.clicked.connect(lambda: self.done(1))
        delete_question2_button.clicked.connect(lambda: self.done(2))
        cancel_button.clicked.connect(lambda: self.done(0))

        buttons_layout.addWidget(delete_question1_button)
        buttons_layout.addWidget(delete_question2_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)


# Rest of the code remains the same as in the previous example


# Example usage of the dialog:
# You need to replace `question1` and `question2` with actual question objects.
# result = dialog.exec()
# if result == 1:
#     print("Delete Question 1")
# elif result == 2:
#     print("Delete Question 2")
# else:
#     print("Cancelled")


# To run the dialog, you need a QApplication instance.
# If you already have one (e.g., in your main application), you don't need to create a new one.
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    session = get_session()
    questions = Question.get_all_questions(session)
    assert len(questions) >= 2
    question1 = questions[0]
    question2 = questions[1]

    dialog = QuestionComparisonDialog(question1, question2)
    result = dialog.exec()
    if result == 1:
        print("Delete Question 1")
    elif result == 2:
        print("Delete Question 2")
    else:
        print("Cancelled")
