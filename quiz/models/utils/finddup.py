from PySide6.QtWidgets import QMessageBox
from quiz.models.Question import Question, get_session


def find_duplicates(widg, user, q: list):
    """Iterate through all questions and search for near duplicates to the current question.
    if a duplicate is found, return the (first) duplicate question, otheerwise return None
    params: q: list
    """
    if not user or user.role != "admin":
        QMessageBox.warning(widg, "Error", "You must be an admin to do this")
        return
    session = get_session()
    current_question = q
    all_questions = Question.get_all_questions(session)

    for question in all_questions:
        if Question.nearly_equal(current_question, question):
            return question
    return None
