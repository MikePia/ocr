# pyside6-rcc resources.qrc -o resources_rc.py
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from .free_quiz_ui import Ui_MainWindow
from quiz.prepstuff.processquestions import get_gpt_response
from quiz.models.Question import (
    Question,
    User,
    get_session,
)


class FreeQuiz(QMainWindow, Ui_MainWindow):
    questions = None
    current_question = -1

    def __init__(self, email=None):
        super(FreeQuiz, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Free Quiz")
        self.setWindowIcon(QIcon("ZSLogo1.png"))
        self.next_btn.clicked.connect(self.next)
        self.actionStart_Quiz.triggered.connect(self.start_quiz)
        self.explanation_btn.clicked.connect(self.get_explanation)
        self.save_notes_btn.clicked.connect(self.save_notes)
        self.login(email)

    def login(self, email):
        email = os.environ.get("MY_USER_EMAIL")
        assert email, "MY_USER_EMAIL environment variable not set"
        self.user = User.get_user(email)

    def get_quiz_questions(self):
        session = get_session()  # Get the SQLAlchemy session
        self.questions = Question.get_all_questions(session)

        session.close()  # Close the session

    def get_explanation(self):
        if self.current_question >= 0 and self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            if not q.explanation:
                explanation = get_gpt_response(q)
                q.explanation = explanation
                session = get_session()
                Question.update_explanation(session, q.explanation, q.id)
                session.close()

            html = f'<html><head/><body><p><span style=" font-size:22pt; font-weight:700; color:#deddda;">GPT Explanation:</span></p><p class="question"><span style=" color:#ffffff;">{q.explanation}</span></p></body></html>'
            self.explanation_edit.setText(html)
            self.update()
            self.explanation_edit.show()

    def start_quiz(self):
        self.get_quiz_questions()
        self.next()

    def clearLayout(self, layout):
        """Utility function to clear all widgets from a layout"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.explanation_edit.clear()

    def save_notes(self):
        print("save notes clicked")

    def next(self):
        if not self.questions:
            self.get_quiz_questions()
            self.current_question = -1

        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            q = self.questions[self.current_question]
            html = f'<html><head/><body><p><span style=" font-size:22pt; font-weight:700; color:#deddda;">Question:</span></p><p class="question"><span style=" color:#ffffff;">{q.question}</span></p></body></html>'
            self.question_label.setText(html)

            self.clearLayout(
                self.answers_verticalLayout
            )  # Clear existing widgets from the layout

            count = 1
            for answer in q.answers:
                if not answer.answer or not answer.answer.strip():  # Skip empty answers
                    continue  # Skip empty answers
                ans = str(count) + ". " + answer.answer
                count += 1
                item_widget = QWidget()  # Create a new widget for each answer
                layout = QHBoxLayout()  # Horizontal layout

                radio_button = QRadioButton()  # Create a radio button
                label = QLabel(ans)  # Create a label

                layout.addWidget(radio_button)  # Add radio button to the layout
                layout.addWidget(label)  # Add label to the layout
                layout.addStretch()  # Add stretch to push everything to the left

                layout.addStretch(
                    1
                )  # Add stretch to fill the remaining horizontal space

                item_widget.setLayout(layout)  # Set the layout for the widget

                self.answers_verticalLayout.addWidget(
                    item_widget
                )  # Add the custom widget to the vertical layout
                self.answers_verticalLayout.setAlignment(
                    item_widget, Qt.AlignTop
                )  # Align the widget to the top

            self.answers_verticalLayout.addStretch(1)

            self.setStyleSheet(
                self.styleSheet()
            )  # Reapply stylesheets to update the style of new widgets
            self.show()
            self.update()
        else:
            # When there are no more questions
            dialog = EndOfQuizDialog(self)
            result = dialog.exec()

            if result == QDialog.Accepted:
                choice, question_number = dialog.get_choice()

                if choice == "start_over":
                    self.current_question = -1
                    self.next()
                elif choice == "specific_question":
                    self.current_question = (
                        question_number - 1
                    )  # Adjusting for zero-based index
                    self.next()
                elif choice == "quit":
                    self.close()  # Close the application


class EndOfQuizDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("End of Quiz")

        # Set up layout
        layout = QVBoxLayout()

        # Add label
        label = QLabel(
            "That is all of the current questions. What would you like to do?"
        )
        layout.addWidget(label)

        # Radio buttons
        self.radio_start_over = QRadioButton("Start over")
        self.radio_specific_question = QRadioButton("Start with question number")
        self.radio_quit = QRadioButton("Quit")

        self.radio_start_over.setChecked(True)  # Default selection

        # Number box
        self.number_box = QSpinBox()
        self.number_box.setMinimum(1)  # Assuming question numbers start from 1

        # Button group
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.radio_start_over)
        self.button_group.addButton(self.radio_specific_question)
        self.button_group.addButton(self.radio_quit)

        # Add widgets to layout
        layout.addWidget(self.radio_start_over)
        layout.addWidget(self.radio_specific_question)
        layout.addWidget(self.number_box)
        layout.addWidget(self.radio_quit)

        # Accept and Cancel buttons
        btn_accept = QPushButton("OK")
        btn_cancel = QPushButton("Cancel")
        btn_accept.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        layout.addWidget(btn_accept)
        layout.addWidget(btn_cancel)

        self.setLayout(layout)

    def get_choice(self):
        if self.radio_start_over.isChecked():
            return "start_over", 0
        elif self.radio_specific_question.isChecked():
            return "specific_question", self.number_box.value()
        else:
            return "quit", 0


def main():
    app = QApplication(sys.argv)
    win = FreeQuiz()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    projectdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(projectdir)
    main()
