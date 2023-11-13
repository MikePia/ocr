import logging
import random

import openai
import os

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Boolean,
    Table,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, joinedload
from dotenv import load_dotenv

from sqlalchemy.types import Enum

from quiz.models.utils.equality import compare_sentences, compare_sets


# from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

logger = logging.getLogger(__name__)

load_dotenv(os.environ["HOME"] + "/.quizzer_rc")
openai.api_key = os.environ["OPEN_API_KEY"]


Base = declarative_base()
dburl = os.environ.get("DATABASE_URL")
assert (
    dburl
), "Environment variable not set. Please place you db connection string DATABASE URL in the file .env"
if not dburl:
    dburl = "sqlite:///quiz.db"
engine = create_engine(dburl)


def get_db_connection():
    engine = create_engine(dburl)
    connection = engine.connect()
    return (
        connection,
        engine.dialect.name,
        engine.dialect.driver,
        engine.url.database,
        engine.url.username,
        engine.url.host,
        engine.url.port,
        engine.url.query,
        engine.url,
    )


def recreate_tables(reallydrop=False):
    if reallydrop:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(Enum("admin", "staff", "student", name="user_roles"), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}')>"

    @classmethod
    def create_new_user(cls, session, username, email, role):
        new_user = cls(username=username, email=email, role=role)
        session.add(new_user)
        return new_user

    @classmethod
    def get_user(cls, email):
        session = get_session()
        user = session.query(cls).filter(cls.email == email).first()
        session.close()
        return user


class QuestionNotes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    notes = Column(String, default="")

    # Assuming 'Question' and 'User' are the names of your other models
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Relationships
    question = relationship("Question", backref="question_notes")
    user = relationship("User", backref="user_notes")

    @classmethod
    def create_or_update_note(cls, notes, question_id, user_id):
        session = get_session()

        try:
            existing_note = (
                session.query(cls)
                .filter_by(question_id=question_id, user_id=user_id)
                .first()
            )

            if existing_note:
                existing_note.notes = notes
            else:
                new_note = cls(notes=notes, question_id=question_id, user_id=user_id)
                session.add(new_note)

            session.commit()

            return existing_note or new_note

        except Exception as e:
            session.rollback()
            logger.exception(str(e))
            raise e

        finally:
            # Ensure the session is closed
            session.close()

    @classmethod
    def get_notes(cls, user_id, question_id):
        session = get_session()

        try:
            # notes = (
            #     session.query(cls)
            #     .filter_by(user_id=user_id, question_id=question_id)
            #     .first()
            # )
            notes = (
                session.query(QuestionNotes)
                .filter_by(user_id=user_id, question_id=question_id)
                .first()
            )
            if notes:
                return notes.notes
            else:
                return None

        except Exception as e:
            session.rollback()
            logger.exception(str(e))
            raise e

        finally:
            session.close()


# Association table for the many-to-many relationship between Tests and Questions
TestQuestions = Table(
    "test_questions",
    Base.metadata,
    Column("test_id", Integer, ForeignKey("tests.id"), primary_key=True),
    Column("question_id", Integer, ForeignKey("questions.id"), primary_key=True),
)


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subject = Column(String)
    level = Column(String)

    # Relationship to questions
    questions = relationship(
        "Question", secondary=TestQuestions, back_populates="tests"
    )

    def __repr__(self):
        return f"<Test(id={self.id}, name='{self.name}', subject='{self.subject}', level='{self.level}')>"



  @classmethod
    def create_test(cls, session, name: str, subject: str, level: str, question_ids=None):
        test = cls(name=name, subject=subject, level=level)
        session.add(test)
        session.commit()

        if question_ids:
            cls.add_to_test(session, test.id, question_ids)

        return test

    @classmethod
    def add_to_test(cls, session, test_id: int, question_ids):
        test = session.query(cls).get(test_id)
        if not test:
            raise ValueError("Test not found")

        if isinstance(question_ids, int):
            question_ids = [question_ids]

        for qid in question_ids:
            question = session.query(Question).get(qid)
            if question:
                test.questions.append(question)

        session.commit()

    @classmethod
    def remove_from_test(cls, session, test_id: int, question_ids):
        test = session.query(cls).get(test_id)
        if not test:
            raise ValueError("Test not found")

        if isinstance(question_ids, int):
            question_ids = [question_ids]

        for qid in question_ids:
            question = session.query(Question).get(qid)
            if question in test.questions:
                test.questions.remove(question)

        session.commit()

    @classmethod
    def get_random_test(cls, session, test_id: int, length: int):
        test = session.query(cls).get(test_id)
        if not test:
            raise ValueError("Test not found")

        if length > len(test.questions):
            raise ValueError("Requested test length exceeds the number of available questions")

        return random.sample(test.questions, length)








class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    explanation = Column(String)

    answers = relationship("Answer", back_populates="question", cascade="all, delete")
    tests = relationship("Test", secondary=TestQuestions, back_populates="questions")

    def __repr__(self):
        return f"<Question(id={self.id}, question='{self.question}', explanation='{self.explanation}')>"

    @classmethod
    def store_question(
        cls, question: str, answers: list, notes=None, correct_answer=None
    ):
        """
        Store the given question and its list of answers.
        The first answer in the list is assumed to be the correct one.
        """
        session = get_session()
        try:
            # Create a new question object
            new_question = Question(
                question=question, answers=[Answer(answer=x) for x in answers]
            )

            # Add the question (with its answers) to the session
            session.add(new_question)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def update_explanation(cls, session, explanation, id):
        try:
            # Retrieve the question with the given ID
            question = session.query(cls).filter_by(id=id).one()

            # Update the explanation
            question.explanation = explanation

            # Commit the changes
            session.commit()
        except Exception as e:
            logger.exception(str(e))
            # Handle any exceptions, possibly log them, and then re-raise
            session.rollback()
            raise

    # Get all questions from the database
    @classmethod
    def get_all_questions(cls, session):
        try:
            # Use joinedload to eagerly load related objects
            questions = (
                session.query(Question).options(joinedload(Question.answers)).all()
            )
            print(len(questions))
            return questions
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def nearly_equal(cls, question1, question2):
        # Compare the question and answer texts
        if compare_sentences(question1.question, question2.question) < 0:
            return False

        # Extract answer texts from both questions
        answers1 = {answer.answer for answer in question1.answers}
        answers2 = {answer.answer for answer in question2.answers}

        # Compare the sets of answers
        return compare_sets(answers1, answers2)

    @classmethod
    def delete_by_id(cls, session, question_id):
        """
        Delete a question by its ID.

        :param session: SQLAlchemy session
        :param question_id: ID of the question to be deleted
        """
        question = session.query(Question).get(question_id)
        if question:
            #  Delete associated notes if there are any
            notes = (
                session.query(QuestionNotes).filter_by(question_id=question_id).all()
            )
            for note in notes:
                session.delete(note)
                # session.commit()

            session.delete(question)
            session.commit()
            return True
        else:
            return False


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    answer = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    is_right_answer = Column(Boolean, default=False)

    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer(id={self.id}, answer='{self.answer}', question_id={self.question_id}, is_right_answer={self.is_right_answer})>"

    @classmethod
    def set_correct_answers(cls, question_id: int, answers: list):
        session = get_session()
        try:
            question = session.query(Question).filter_by(id=question_id).one()
            answers = [x.strip() for x in answers]
            for answer in question.answers:
                if answer.answer.strip() in answers:
                    answer.is_right_answer = True
                else:
                    answer.is_right_answer = False
            session.commit()
        except Exception as e:
            session.rollback()
            logger.exception(str(e))
            raise e
        finally:
            session.close()

    @classmethod
    def get_correct_answers(self, question_id):
        session = get_session()
        try:
            answers = (
                session.query(Answer)
                .filter_by(question_id=question_id, is_right_answer=True)
                .all()
            )
            return answers
        except Exception as e:
            session.rollback()
            logger.exception(str(e))
            raise e
        return []

    def __repr__(self):
        return f"<Answer(id={self.id}, answer='{self.answer}', question_id={self.question_id}, is_right_answer={self.is_right_answer})>"
