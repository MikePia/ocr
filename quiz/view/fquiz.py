# pyside6-rcc resources.qrc -o resources_rc.py
import os
import sys

from PySide6.QtCore import Qt, QSettings, QRect, QByteArray, QPoint
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QComboBox,
)


from .free_quiz_ui import Ui_MainWindow
from quiz.prepstuff.processquestions import get_gpt_response
from quiz.models.Question import (
    Question,
    QuestionNotes,
    User,
    get_session,
    Answer,
)

COMPANY = "ZeroSubstance"


class FreeQuiz(QMainWindow, Ui_MainWindow):
    questions = None
    current_question = -1
    user = None
    answer_items = []
    show_answers_bool = False

    def __init__(self, email=None):
        super(FreeQuiz, self).__init__()
        self.setupUi(self)
        self.init_window_placement()
        self.setWindowTitle("Free Quiz")
        self.setWindowIcon(QIcon("ZSLogo1.png"))

        self.next_btn.clicked.connect(self.next)
        self.previous_btn.clicked.connect(self.previous)
        self.explanation_btn.clicked.connect(self.get_explanation)
        self.save_notes_btn.clicked.connect(self.save_notes)
        self.show_answer_btn.clicked.connect(self.show_answer)
        self.show_answers_cb.clicked.connect(self.show_answers)

        self.actionStart_Quiz.triggered.connect(self.start_quiz)
        self.actionStart_Quiz.triggered.connect(self.menu_start)
        self.actionSet_Item_Correct.triggered.connect(self.set_item_correct)
        self.actionRegenerate.triggered.connect(self.regenerate)

        self.login(email)

    def init_window_placement(self):
        """Initialize window placement using QSettings."""
        self.settings = QSettings(COMPANY, "FreeQuizApp")
        self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        self.restoreState(self.settings.value("windowState", QByteArray()))

        # restoreGeometry and restoreState not working. I think I remember this is an Ubuntu problem. Here is a workaround
        self.move(
            int(self.settings.value("x", int())), int(self.settings.value("y", int()))
        )

    def closeEvent(self, event):
        """Save window state when the application is closed."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        self.settings.setValue("x", self.x())
        self.settings.setValue("y", self.y())

        super(FreeQuiz, self).closeEvent(event)

    def menu_start(self):
        self.current_question = -1
        self.next()

    def get_selected_answers(self):
        answers = []
        for i in range(len(self.answer_items)):
            answer = self.answer_items[i]
            if answer[0].isChecked():
                answers.append([i, answer[1][2:].strip()])
        return answers

    def set_item_correct(self):
        if self.current_question >= 0 and self.current_question < len(self.questions):
            selected_answers = self.get_selected_answers()
            q = self.questions[self.current_question]
            Answer.set_correct_answers(q.id, [x[1] for x in selected_answers])

    def regenerate(self):
        self.get_explanation(force=True)

    def userSelect(self):
        session = get_session()
        dialog = UserLoginDialog(session)
        if dialog.exec():
            selected_user = dialog.user
            if selected_user:
                print(f"Selected User: {selected_user.username}")
                self.user = selected_user

    def login(self, email):
        self.user = User.get_user(email)

    def get_quiz_questions(self):
        session = get_session()  # Get the SQLAlchemy session
        self.questions = Question.get_all_questions(session)

        session.close()  # Close the session

    def get_explanation(self, force=False):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            if self.current_question >= 0 and self.current_question < len(
                self.questions
            ):
                q = self.questions[self.current_question]
                if not q.explanation or force:
                    explanation = get_gpt_response(q)
                    q.explanation = explanation
                    session = get_session()
                    Question.update_explanation(session, q.explanation, q.id)
                    session.close()

                html = f'<html><head/><body><p><span style=" font-size:22pt; font-weight:700; color:#deddda;">GPT Explanation:</span></p><p class="question"><span style=" color:#ffffff;">{q.explanation}</span></p></body></html>'
                self.explanation_edit.setText(html)
                self.update()
                self.explanation_edit.show()
        finally:
            QApplication.restoreOverrideCursor()  # Restore the original cursor

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
        self.notes_edit.clear()
        self.answer_items.clear()
        self.show_answers_le.clear()

    def save_notes(self):
        if (
            self.current_question >= 0
            and self.current_question < len(self.questions)
            and self.user
        ):
            # user = User.get_user(self.user_email)
            q = self.questions[self.current_question]
            notes = self.notes_edit.toPlainText()
            q.notes = notes
            QuestionNotes.create_or_update_note(notes, q.id, self.user.id)
        else:
            # Qt dialog showing failure
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Unable to save notes.")
            msg.setInformativeText(
                "Please ensure you have selected a valid question and are logged in."
            )
            msg.exec_()

    def show_answer(self):
        if self.current_question >= 0 and self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            answers = Answer.get_correct_answers(q.id)
            dbanswers = [x.answer.strip() for x in answers]
            printed_answers = []
            for i, item in enumerate(self.answer_items):
                if item[1][2:].strip() in dbanswers:
                    printed_answers.append(
                        f"{chr(i + ord('A'))}) {item[1][2:].strip()}"
                    )
            a = ": ".join(printed_answers)
            self.show_answers_le.setText(a)
            self.update()
            self.show()

    def show_answers(self, val):
        self.show_answers_bool = val
        if val:
            self.show_answer()

    def previous(self):
        if self.current_question > 0 and self.current_question < len(self.questions):
            self.current_question -= 2
        else:
            self.current_question = -1

        self.next()

    def next(self):
        if not self.questions:
            self.get_quiz_questions()
            self.current_question = -1

        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            q = self.questions[self.current_question]
            html = f'<html><head/><body><p><span style=" font-size:22pt; font-weight:700; color:#deddda;">Question:</span></p><p class="question"><span style=" color:#ffffff;">{q.question}</span></p></body></html>'
            self.question_label.setText(html)

            self.clearLayout(self.answers_verticalLayout)
            count = 0
            html = f'<html><head/><body><p><span style=" font-size:22pt; font-weight:700; color:#deddda;">Answers:</span></p><p class="question"><span style=" color:#ffffff;"><hr></span></p></body></html>'
            new_answers_label = QLabel(html)
            # self.answers_label.setText(html)
            self.answers_verticalLayout.addWidget(new_answers_label)
            self.answers_verticalLayout.setAlignment(new_answers_label, Qt.AlignTop)
            for answer in q.answers:
                if not answer.answer or not answer.answer.strip():  # Skip empty answers
                    continue  # Skip empty answers
                ans = chr(count + ord("A")) + ". " + answer.answer
                count += 1

                # Create a new widget for each answer
                item_widget = QWidget()
                layout = QHBoxLayout()

                radio_button = QRadioButton()
                self.answer_items.append([radio_button, ans])
                label = QLabel(ans)

                layout.addWidget(radio_button)
                layout.addWidget(label)
                layout.addStretch()

                layout.addStretch(1)

                item_widget.setLayout(layout)

                item_widget.setStyleSheet(
                    "color: rgb(0, 0, 0); background-color: rgb(153, 193, 241);"
                )
                self.answers_verticalLayout.addWidget(item_widget)
                self.answers_verticalLayout.setAlignment(item_widget, Qt.AlignTop)

            if self.user:
                notes = QuestionNotes.get_notes(self.user.id, q.id)
                if notes:
                    self.notes_edit.setText(notes)
                else:
                    self.notes_edit.clear()

            self.answers_verticalLayout.addStretch(1)

            self.setStyleSheet(self.styleSheet())
            if self.show_answers_bool:
                self.show_answer()
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


# Assume User is your SQLAlchemy model
# from your_model_file import User


class UserLoginDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session  # SQLAlchemy session
        self.user = None  # Current user

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # List of users
        self.user_list = QListWidget(self)
        self.load_users()
        layout.addWidget(self.user_list)

        # New user form
        self.username_edit = QLineEdit(self)
        self.email_edit = QLineEdit(self)
        self.role_combo = QComboBox(self)
        self.role_combo.addItems(["admin", "staff", "student"])  # Adding role options
        new_user_layout = QHBoxLayout()
        new_user_layout.addWidget(QLabel("Username:"))
        new_user_layout.addWidget(self.username_edit)
        new_user_layout.addWidget(QLabel("Email:"))
        new_user_layout.addWidget(self.email_edit)
        new_user_layout.addWidget(QLabel("Role:"))
        new_user_layout.addWidget(self.role_combo)
        layout.addLayout(new_user_layout)

        # Buttons
        self.select_button = QPushButton("Select User", self)
        self.select_button.clicked.connect(self.select_user)
        self.create_button = QPushButton("Create New User", self)
        self.create_button.clicked.connect(self.create_user)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.create_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_users(self):
        self.user_list.clear()
        users = self.session.query(User).all()
        for user in users:
            self.user_list.addItem(f"{user.username} ({user.email})")

    def select_user(self):
        selected_items = self.user_list.selectedItems()
        if selected_items:
            selected_user = selected_items[0].text()
            username = selected_user.split(" (")[0]
            self.user = self.session.query(User).filter_by(username=username).first()
            self.accept()

    def create_user(self):
        username = self.username_edit.text()
        email = self.email_edit.text()
        role = self.role_combo.currentText()

        if username and email:
            new_user = User.create_new_user(
                self.session, username=username, email=email, role=role
            )
            self.session.commit()
            QMessageBox.information(
                self, "User Created", f"User '{username}' created successfully."
            )
            self.load_users()
        else:
            QMessageBox.warning(self, "Incomplete Form", "Please fill in all fields.")


def main(email=None):
    app = QApplication(sys.argv)
    win = FreeQuiz(email)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
