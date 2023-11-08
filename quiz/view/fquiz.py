# pyside6-rcc resources.qrc -o resources_rc.py
import logging
import sys

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtGui import QIcon, QPixmap
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
    QMessageBox,
)
from quiz.view.create_question import QuizProcessingDialog
from quiz.view.login_dlg import UserLoginDialog
from quiz.view.question_compare_dlg import QuestionComparisonDialog


from .free_quiz_ui import Ui_MainWindow
from quiz.prepstuff.processquestions import get_gpt_response
from quiz.models.Question import (
    Question,
    QuestionNotes,
    get_session,
    Answer,
)

logger = logging.getLogger(__name__)

COMPANY = "ZeroSubstance"
APPNAME = "FreeQuizApp"


class FreeQuiz(QMainWindow, Ui_MainWindow):
    questions = None
    current_question = -1
    user = None
    answer_items = []
    show_answers_bool = False

    def __init__(self, email=None):
        super(FreeQuiz, self).__init__()
        self.setupUi(self)
        self.settings = QSettings(COMPANY, APPNAME)
        self.init_window_placement()
        self.setWindowTitle("Free Quiz")
        self.setWindowIcon(QIcon("ZSLogo1.png"))

        self.next_btn.clicked.connect(self.next)
        self.previous_btn.clicked.connect(self.previous)
        self.explanation_btn.clicked.connect(self.get_explanation)
        self.save_notes_btn.clicked.connect(self.save_notes)
        self.show_answer_btn.clicked.connect(self.show_answer)
        self.show_answers_cb.clicked.connect(self.show_answers)
        self.submit_btn.clicked.connect(self.submit_question)

        self.actionStart_Quiz.triggered.connect(self.start_quiz)
        self.actionStart_Quiz.triggered.connect(self.menu_start)
        self.actionUser_Login.triggered.connect(self.userSelect)
        self.actionSet_Item_Correct.triggered.connect(self.set_item_correct)
        self.actionRegenerate.triggered.connect(self.regenerate)
        self.actionFind_Duplicates.triggered.connect(self.find_duplicates)
        self.actionCreate_Q.triggered.connect(self.create_question)
        self.actionDelete_Question.triggered.connect(self.delete_question)

        self.login(email)

    def init_window_placement(self):
        """Initialize window placement using QSettings."""

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

    def find_duplicates(self):
        """Iterate through all questions and search for near duplicates to the current question.
        If found, pop up a dialog offering to delete one or the other question. Short circuit if
        the user chooses to delete the current question.
        """
        if not self.user or self.user.role != "admin":
            QMessageBox.warning(self, "Error", "You must be an admin to do this")
            return
        session = get_session()
        current_question = self.questions[self.current_question]
        all_questions = Question.get_all_questions(session)

        try:
            for question in all_questions:
                if question.id == current_question.id:
                    continue  # Skip comparison with itself

                if Question.nearly_equal(current_question, question):
                    dialog = QuestionComparisonDialog(current_question, question, self)
                    result = dialog.exec()

                    if result == 1:
                        # Delete current question and exit the loop
                        Question.delete_by_id(session, current_question.id)
                        self.current_question = -1
                        return
                    elif result == 2:
                        # Delete the other question
                        Question.delete_by_id(session, question.id)
            QMessageBox.information(self, "Success", "Find Duplicates Done")
        except Exception as e:
            logger.exception(str(e))
            QMessageBox.warning(self, "Error", "Error finding duplicates")
            session.rollback()
        finally:
            session.close()
            self.get_quiz_questions()

    def create_question(self):
        dialog = QuizProcessingDialog(self.user)
        x = dialog.exec()
        print(x)

    def delete_question(self):
        if not self.user or self.user.role != "admin":
            QMessageBox.warning(self, "Error", "You must be an admin to do this")
            return
        if self.current_question >= 0 and self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            session = get_session()
            Question.delete_by_id(session, q.id)
            session.close()
            self.get_quiz_questions()
            self.next()
        else:
            QMessageBox.warning(self, "Error", "No question selected")
            return
        return

    def userSelect(self):
        session = get_session()
        dialog = UserLoginDialog(session, user=self.user)
        if dialog.exec():
            selected_user = dialog.user
            if selected_user:
                self.user = selected_user

    def login(self, email):
        """This is the automatic login only. Only used by __init__"""
        if self.settings.value("save_choice", False):
            self.user = self.settings.value("selected_user")
        if not self.user:
            self.userSelect()

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
            return dbanswers

    def show_answers(self, val):
        self.show_answers_bool = val
        if val:
            self.show_answer()

    def submit_question(self):
        if self.current_question >= 0 and self.current_question < len(self.questions):
            selected_answers = self.get_selected_answers()
            right_answers = self.show_answer()
            success = {x[1].strip() for x in selected_answers} == set(right_answers)
            self.get_explanation()
            if success:
                msg = (
                    '<p> <span style="font-size:22pt; font-weight:700; color:#deddda;"> '
                    "Congratulations!! </span> </p><p> you are correct!</p>"
                )
            else:
                msg = "<p>Sorry, you are incorrect.</p>"

            submitinfo = QMessageBox.information(
                self, "Success" if success else "Incorrect", msg
            )
            if success:
                submitinfo.setIconPixmap(QPixmap("images/confetti.png"))

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


def main(email=None):
    app = QApplication(sys.argv)
    win = FreeQuiz(email)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
