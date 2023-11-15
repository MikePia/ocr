# pyside6-rcc resources.qrc -o resources_rc.py
import html
import logging
import sys

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)

# include <QString>
from quiz.view.create_question import EditQuestionDialog, QuizProcessingDialog
from quiz.view.loadcsv_yesno import LoadCsvYesNo
from quiz.view.login_dlg import UserLoginDialog
from quiz.view.question_compare_dlg import QuestionComparisonDialog
from quiz.view.openai_options import Openai
from quiz.view.create_test import TestDialog

from .quiz_ui import Ui_MainWindow
from quiz.prepstuff.processquestions import get_gpt_response
from quiz.models.Question import (
    Question,
    QuestionNotes,
    get_session,
    Answer,
    recreate_tables,
)

logger = logging.getLogger(__name__)

COMPANY = "ZeroSubstance"
APPNAME = "FreeQuizApp"


class FreeQuiz(QMainWindow, Ui_MainWindow):
    default_gpt_engine = "gpt-4-1106-preview"
    questions = None
    current_question = -1
    selected_questions = []
    user = None
    answer_items = []
    show_answers_bool = False

    def __init__(self, email=None):
        super(FreeQuiz, self).__init__()
        self.setupUi(self)
        self.settings = QSettings(COMPANY, APPNAME)
        self.settings.setValue("default_gpt_engine", self.default_gpt_engine)
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

        # User actions
        self.actionStart_Quiz.triggered.connect(self.start_quiz)
        self.actionUser_Login.triggered.connect(self.userSelect)
        self.actionQuit.triggered.connect(self.quit)
        self.actionOpenai_opt.triggered.connect(self.openai_opt)
        self.actionSearch_for_question.triggered.connect(self.search_for_question)
        self.actionTest_Manager.triggered.connect(self.test_manager)
        self.actionTake_Test.triggered.connect(self.take_test)

        # Admin actions
        self.actionStart_Quiz.triggered.connect(self.menu_start)
        self.actionSet_Item_Correct.triggered.connect(self.set_item_correct)
        self.actionRegenerate.triggered.connect(self.regenerate)
        self.actionFind_Duplicates.triggered.connect(self.find_duplicates)
        self.actionCreate_Q.triggered.connect(self.create_question)
        self.actionDelete_Question.triggered.connect(self.delete_question)
        self.actionLoad_csv.triggered.connect(self.load_csv)
        self.actionEdit_this_question.triggered.connect(self.edit_question)

        recreate_tables()
        self.get_quiz_questions()

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
        self.selected_questions = []
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
            self.current_question -= 1
            self.next()

            # Reselect the selected_answers
            for answer in selected_answers:
                answer_index = answer[0]
                answer_widget = self.answer_items[answer_index][0]
                answer_widget.setChecked(True)

    def regenerate(self):
        self.get_explanation(force=True)

    def find_duplicates(self):
        """Iterate through all questions and search for near duplicates to the current question.
        If found, pop up a dialog offering to delete one or the other question. Short circuit if
        the user chooses to delete the current question.
        """
        self.selected_questions = []
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
        dialog.exec()

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

    def load_csv(self):
        dontask = self.settings.value("load_csv_do_not_ask_again", False)
        if not dontask or dontask == "false":
            dialog = LoadCsvYesNo()
            dialog.exec()

            if dialog.do_not_ask_again:
                self.settings.setValue("load_csv_do_not_ask_again", True)
            else:
                self.settings.setValue("load_csv_do_not_ask_again", False)

            if dialog.user_choice:
                self.process_csv()
        else:
            self.process_csv()

    def edit_question(self):
        if self.current_question >= 0 and self.current_question < len(self.questions):
            if not self.user or self.user.role != "admin":
                QMessageBox.warning(self, "Error", "You must be an admin to do this")
                return
            # Get the current question
            question = self.questions[self.current_question]
            dialog = EditQuestionDialog(self.user, question, self)
            dialog.exec()

            session = get_session()
            self.questions = Question.get_all_questions(session)
            session.close()

            self.current_question -= 1
            self.next()

    def process_csv(self):
        csv_file, _ = QFileDialog.getOpenFileName(
            self, "Open csv file", "", "CSV Files (*.csv)"
        )
        if not csv_file:
            return
        with open(csv_file, "r") as f:
            lines = f.readlines()
        # Check if the first column is a list of images
        req = ["question", "answer1", "answer2", "answer3", "answer4"]
        opt = ["notes", "correct_answer"]
        columns = lines[0].split(",")
        columns = [x.strip().lower() for x in columns]
        if any(x not in columns for x in req):
            msg = (
                '<html><head/><body><p><span style="font-size:22pt; font-weight:700; color:#deddda;">'
                "Unrecognized csv format </span></p> "
                "<p>Required fields for this csv are: </p> "
                "<p><b>[question, answer1, answer2, answer3, answer4, ...]</b></p> "
                "</span></body></html>"
            )
            QMessageBox.information(self, "Unrecognized csv format", msg)
            self.settings.setValue("load_csv_do_not_ask_again", False)
            return
        # map the ruquired and optional fields to their index in the csv
        col_mapping = {
            field: columns.index(field) for field in req + opt if field in columns
        }
        for line in lines[1:]:
            line = line.split(",")
            question = line[col_mapping["question"]]
            answers = line[col_mapping["answer1"] : col_mapping["answer4"] + 1]
            answers = [x.strip() for x in answers]
            notes = line[col_mapping.get("notes")] if col_mapping.get("notes") else None
            correct_answer = (
                line[col_mapping.get("correct_answer", -1)]
                if col_mapping.get("correct_answer")
                else None
            )
            if correct_answer:
                correct_answer = correct_answer.strip().lower()
            else:
                correct_answer = None
            Question.store_question(question, answers, notes, correct_answer)

    def userSelect(self):
        session = get_session()
        dialog = UserLoginDialog(session, user=self.user)
        if dialog.exec():
            selected_user = dialog.user
            if selected_user:
                self.user = selected_user

    def quit(self):
        self.close()

    def openai_opt(self):
        dialog = Openai()
        dialog.exec()

    def search_for_question(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Search for a question")
        dialog.setLabelText("Enter the text to search for:")
        dialog.resize(600, 200)

        ok = dialog.exec()
        text = dialog.textValue()

        if ok:
            # Search questions for matches
            self.get_quiz_questions()
            qs = [
                i
                for i, x in enumerate(self.questions)
                if text.lower() in x.question.lower()
            ]
            ids = [x.id for x in self.questions if text.lower() in x.question.lower()]

            QMessageBox.information(
                self, "Search Results", f"Found {len(qs)} questions. Ids: {ids}"
            )
            self.selected_questions = qs
            self.next()

    def test_manager(self):
        dialog = TestDialog()
        dialog.exec()

    def take_test(self):
        html_text = (
            "<html><head/><body>"
            '<p><span style=" font-size:22pt; font-weight:700; color:#deddda;">Test Unimplemented</span></p>'
            '<p><span style=" color:#cccccc;">I created this tool to pass a few Freelancer quizes and to try out PySide6. If '
            "there is any interest in developing features on this app, improving it, or getting an easy PyPi release, "
            "please contact me by opening an issue in github <hr><br>"
            '<a href="https://github.com/MikePia/quizzer" style="color: white; text-decoration: none;">https://github.com/MikePia/quizzer</a>'
            "</span></p></body></html>"
        )
        QMessageBox.information(self, "Test is Unimplemented", html_text)

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

    def parse_correct_answer(self, explanation):
        ans_text = explanation.split(".")[0]
        if ans_text.lower().startswith("the correct answer is "):
            ans_text = ans_text[22:]
        for ans in [x[1] for x in self.answer_items]:
            if ans[2:].strip().lower() in ans_text.lower():
                q = self.questions[self.current_question]
                Answer.set_correct_answers(q.id, [ans[2:].strip()])

                self.show_answers_le.setText(ans)
                break

    def get_explanation(self, force=False):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:
            if self.current_question >= 0 and self.current_question < len(
                self.questions
            ):
                q = self.questions[self.current_question]
                if not q.explanation or force:
                    val = self.settings.value("user_gpt_engine")
                    if val and val == "None":
                        return
                    explanation = get_gpt_response(q)
                    q.explanation = explanation
                    session = get_session()
                    Question.update_explanation(session, q.explanation, q.id)
                    session.close()
                encoded_explanation = html.escape(q.explanation)
                test_encode = q.explanation.encode("utf-8")
                html_text = f'<html><head/><body><p><span style=" font-size:22pt; font-weight:700; color:#deddda;">GPT Explanation:</span></p><p class="question"><span style=" color:#ffffff;">{encoded_explanation}</span></p></body></html>'
                self.explanation_edit.setText(html_text)
                if not self.show_answers_le.text():
                    self.parse_correct_answer(q.explanation)
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
            # self.update()
            # self.repaint()
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

            QMessageBox.information(self, "Success" if success else "Incorrect", msg)

    def previous(self):
        if (
            not self.selected_questions
            and self.current_question > 0
            and self.current_question < len(self.questions)
        ):
            self.current_question -= 2
        else:
            self.current_question = -1

        self.next()

    def next(self):
        if not self.questions:
            self.get_quiz_questions()
            self.current_question = -1
        if self.selected_questions:
            self.current_question = self.selected_questions.pop(0) - 1

        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            q = self.questions[self.current_question]
            html_text = f'<html><head/><body><p><span style=" font-size:22pt; font-weight:700; color:#deddda;">Question:</span></p><p class="question"><span style=" color:#ffffff;">{q.question}</span></p></body></html>'
            self.question_label.setText(html_text)

            self.clearLayout(self.answers_verticalLayout)
            count = 0
            html_text = '<html><head/><body><p><span style=" font-size:22pt; font-weight:700; color:#deddda;">Answers:</span></p><p class="question"><span style=" color:#ffffff;"><hr></span></p></body></html>'
            new_answers_label = QLabel(html_text)
            # self.answers_label.setText(html_text)
            self.answers_verticalLayout.addWidget(new_answers_label)
            self.answers_verticalLayout.setAlignment(new_answers_label, Qt.AlignTop)
            self.statusBar().showMessage(
                "Question # "
                + str(self.current_question)
                + " Question id: "
                + str(q.id)
            )
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

            # Set the focus on the first answer
            self.answer_items[0][0].setFocus()

            self.show()
            self.update()
        else:
            if self.selected_questions:
                # There are questions on the short list
                return
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
        self.number_box.setMinimum(1)
        self.number_box.setMaximum(99999)

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
