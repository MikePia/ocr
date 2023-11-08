from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)
import sys

from quiz.models.Question import get_session, User

# Assume User is your SQLAlchemy model
# from your_model_file import User

COMPANY = "ZeroSubstance"
APPNAME = "FreeQuizApp"


class UserLoginDialog(QDialog):
    def __init__(self, session, parent=None, user=None):
        super().__init__(parent)
        self.session = session  # SQLAlchemy session
        self.user = user
        self.settings = QSettings(COMPANY, APPNAME)

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
        self.role_cb = QComboBox()
        self.role_cb.addItems(["admin", "staff", "student"])
        self.save_choice = QCheckBox("Save Choice")
        new_user_layout = QHBoxLayout()
        new_user_layout.addWidget(QLabel("Username:"))
        new_user_layout.addWidget(self.username_edit)
        new_user_layout.addWidget(QLabel("Email:"))
        new_user_layout.addWidget(self.email_edit)
        new_user_layout.addWidget(QLabel("Role:"))
        new_user_layout.addWidget(self.role_cb)
        new_user_layout.addWidget(self.save_choice)
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
        for i, user in enumerate(users):
            self.user_list.addItem(f"{user.username} : {user.email} : {user.role}")
            if (
                user.username == self.user.username
                and user.email == self.user.email
                and user.role == self.user.role
            ):
                self.user_list.setCurrentRow(i)

    def select_user(self):
        selected_items = self.user_list.selectedItems()
        if selected_items:
            selected_user = selected_items[0].text()
            # Assuming username is unique and extracting it from the list item text
            username = selected_user.split(" (")[0]
            self.user = self.session.query(User).filter_by(username=username).first()
            self.accept()
            if self.save_choice.isChecked():
                # self.settings.setValue("selected_username", username)
                self.settings.setValue("save_choice", True)
                self.settings.setValue("selected_user", self.user)

            print()

    def create_user(self):
        username = self.username_edit.text()
        email = self.email_edit.text()
        # role = self.role_cb.text()
        role = self.role_cb.currentText()

        if username and email and role:
            # Assuming User model has username, email, role fields
            new_user = User(username=username, email=email, role=role)
            self.session.add(new_user)
            self.session.commit()
            QMessageBox.information(
                self, "User Created", f"User '{username}' created successfully."
            )
            self.load_users()
        else:
            QMessageBox.warning(self, "Incomplete Form", "Please fill in all fields.")


if __name__ == "__main__":
    # Sample usage
    app = QApplication(sys.argv)
    session = get_session()  # SQLAlchemy session
    dialog = UserLoginDialog(session)
    if dialog.exec():
        selected_user = dialog.user
        if selected_user:
            print(f"Selected User: {selected_user.username}")
    sys.exit(app.exec())
