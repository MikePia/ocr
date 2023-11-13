import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
    QMessageBox,
)

from quiz.models.Question import Question, Test, get_session


class TestDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Layouts

        self.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.987, y2:0.579545, stop:0.028065 rgba(30, 82, 139, 255), stop:0.731343 rgba(12, 34, 89, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "\n"
            ""
        )

        main_layout = QVBoxLayout(self)
        form_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Widgets for creating a test
        self.name_input = QLineEdit(self)
        self.subject_input = QLineEdit(self)
        self.level_input = QLineEdit(self)
        create_button = QPushButton("Create Test", self)
        create_button.clicked.connect(self.create_test)

        # Add widgets to form layout
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Subject:"))
        form_layout.addWidget(self.subject_input)
        form_layout.addWidget(QLabel("Level:"))
        form_layout.addWidget(self.level_input)
        form_layout.addWidget(create_button)

        # List widget to display tests
        self.tests_list = QListWidget(self)
        self.populate_tests_list()  # Populate with existing tests

        # Delete button
        delete_button = QPushButton("Delete Selected Test", self)
        delete_button.clicked.connect(self.delete_test)

        button_layout.addWidget(delete_button)

        self.edit_test_button = QPushButton("Edit Selected Test", self)
        self.edit_test_button.clicked.connect(self.edit_selected_test)
        button_layout.addWidget(self.edit_test_button)

        # Add layouts to main layout
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.tests_list)
        main_layout.addLayout(button_layout)

        self.setWindowTitle("Test Manager")

    def create_test(self):
        name = self.name_input.text()
        subject = self.subject_input.text()
        level = self.level_input.text()
        session = get_session()
        Test.create_test(session, name, subject, level)
        session.close()
        print(f"Creating Test: {name}, {subject}, {level}")
        self.populate_tests_list()

    def delete_test(self):
        # Logic to delete the selected test
        # You need to add your logic here to actually delete the test
        selected_item = self.tests_list.selectedItems()
        if not selected_item:
            QMessageBox.warning(self, "Warning", "Please select a test to delete.")
            return

        test_to_delete = selected_item[0].text()
        # Add database logic here to delete the test
        test_id = int(test_to_delete.split(":")[0].strip())
        session = get_session()
        Test.delete_test(session, test_id)
        session.close()

        # Delete the test from the list widget
        self.tests_list.takeItem(self.tests_list.row(selected_item[0]))

        # Add logic here to fetch tests from the database
        self.populate_tests_list()

    def populate_tests_list(self):
        # Populate the list widget with tests
        self.tests_list.clear()
        # Add logic here to fetch tests from the database
        session = get_session()
        tests = Test.getTests(session)
        self.tests = tests
        for test in tests:
            test = f"{test.id}: {test.name} - {test.subject} - {test.level} - {len(test.questions)} questions"

            self.tests_list.addItem(test)
        session.close()

    def edit_selected_test(self):
        selected_items = self.tests_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a test to edit.")
            return
        test_to_edit = selected_items[0].text()  # Get the test ID or name
        id = int(test_to_edit.split(":")[0])
        t = [x for x in self.tests if x.id == id]
        if t:
            edit_dialog = EditTestDialog(t[0], self)
            edit_dialog.exec()


class EditTestDialog(QDialog):
    def __init__(self, test, parent=None):
        super().__init__(parent)
        self.test = test
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        # List widget for questions in the test but make it multiselect
        self.test_questions_list = QListWidget(self)
        self.test_questions_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.populate_test_questions_list()

        # List widget for other questions but make it multiselect
        self.other_questions_list = QListWidget(self)
        self.other_questions_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.populate_other_questions_list()

        # Buttons to move questions between lists
        btn_layout = QVBoxLayout()
        self.add_btn = QPushButton("<< Add", self)
        self.add_btn.clicked.connect(self.add_questions)
        self.remove_btn = QPushButton("Remove>>", self)
        self.remove_btn.clicked.connect(self.remove_questions)

        btn_layout.addStretch()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addStretch()

        layout.addWidget(self.test_questions_list)
        layout.addLayout(btn_layout)
        layout.addWidget(self.other_questions_list)

        self.setWindowTitle(f"Edit Test: {self.test}")

    def populate_test_questions_list(self):
        self.test_questions_list.clear()
        test_questions = self.test.questions
        for question in test_questions:
            self.test_questions_list.addItem(f"{question.id}: {question.question}")

    def populate_other_questions_list(self):
        self.other_questions_list.clear()
        question_ids = [question.id for question in self.test.questions]
        session = get_session()
        other_questions = Question.get_all_other_questions(session, question_ids)
        for question in other_questions:
            self.other_questions_list.addItem(f"{question.id}: {question.question}")

    def add_questions(self):
        # Logic to add selected questions from other_questions_list to test_questions_list
        # Update the database accordingly
        # get the selected items from other_questions_list
        selected_items = self.other_questions_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a question to add.")
            return
        # add the selected items to the current Test
        session = get_session()
        question_ids = [int(x.text().split(":")[0].strip()) for x in selected_items]
        list_items = [x.text() for x in selected_items]
        self.test_questions_list.addItems(list_items)
        Test.add_to_test(session, self.test.id, question_ids)
        # Remove the questions from the other_questions_list
        for item in selected_items:
            self.other_questions_list.takeItem(self.other_questions_list.row(item))
        session.close()

    def remove_questions(self):
        # Logic to remove selected questions from test_questions_list
        # Update the database accordingly
        selected_items = self.test_questions_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a question to remove.")
            return
        # remove the selected items from the current Test
        session = get_session()
        question_ids = [int(x.text().split(":")[0].strip()) for x in selected_items]
        list_items = [x.text() for x in selected_items]
        self.other_questions_list.addItems(list_items)
        Test.remove_from_test(session, self.test.id, question_ids)
        # Remove the questions from the test_questions_list
        for item in selected_items:
            self.test_questions_list.takeItem(self.test_questions_list.row(item))
        session.close()


def main():
    app = QApplication(sys.argv)
    dialog = TestDialog()
    dialog.exec()


if __name__ == "__main__":
    main()
