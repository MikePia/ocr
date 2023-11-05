import logging

import openai
import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, joinedload
from dotenv import load_dotenv

from sqlalchemy.types import Enum

logger = logging.getLogger(__name__)

load_dotenv(os.environ["HOME"] + "/.chatgpt")
openai.api_key = os.environ["OPEN_API_KEY"]


Base = declarative_base()
engine = create_engine("postgresql://postgres:s3cr3tp4ssw0rd@localhost:5432/company")


def get_db_connection():
    engine = create_engine(
        "postgresql://postgres:s3cr3tp4ssw0rd@localhost:5432/company"
    )
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
        Base.metadata.drop_all(engine)  # Drop existing tables
    Base.metadata.create_all(
        engine
    )  # Create tables again with new fields and constraints


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
    def create_note(cls, notes, question_id, user_id):
        session = get_session()  # Open a session

        try:
            new_note = QuestionNotes.create_note(
                session, "Note content", question_id, user_id
            )
            # You can add more operations here
            session.commit()  # Commit the session to save all changes
        except Exception as e:
            session.rollback()  # Roll back in case of an error
            logger.execption(str(e))
            raise  # Re-raise the exception to handle it as needed
        finally:
            session.close()  # Ensure the session is closed
            return new_note


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    explanation = Column(Text)

    answers = relationship("Answer", back_populates="question")

    def __repr__(self):
        return f"<Question(id={self.id}, question='{self.question}', explanation='{self.explanation}')>"

    @classmethod
    def store_question(cls, question: str, answers: list):
        """
        Store the given question and its list of answers.
        The first answer in the list is assumed to be the correct one.
        """
        session = get_session()
        try:
            # Create a new question object
            new_question = cls(question=question)

            # Append answers to the question, marking the first one as the right answer
            for idx, answer_text in enumerate(answers):
                new_answer = Answer(answer=answer_text, is_right_answer=(idx == 0))
                new_question.answers.append(new_answer)

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
            return questions
        except Exception as e:
            session.rollback()
            raise e


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    answer = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    is_right_answer = Column(Boolean, default=False)

    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer(id={self.id}, answer='{self.answer}', question_id={self.question_id}, is_right_answer={self.is_right_answer})>"
