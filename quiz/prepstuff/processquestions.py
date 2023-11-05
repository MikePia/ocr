import logging
import re
import csv
import openai
import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, joinedload
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine

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


def process_csv(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            q = row[0]
            a = row[1].split(",")
            answers = []
            for i in a:
                if not i:
                    continue
                answers.append(i.strip())

            # questions.append((q, answers))
            Question.store_question(q, a)
            print(q)
    return None


def view_questions():
    session = get_session()
    questions = Question.get_all_questions(session)
    ix = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
    for question in questions:
        print()
        print(question.question)
        for i, answer in enumerate(question.answers):
            print(f" {ix[i]}. {answer.answer}")

    # session.close()
    print("done")
    return None


def print_questions_with_answers(session):
    # Query all questions, joined with their answers
    questions = session.query(Question).all()

    for question in questions:
        print(f"Question ID: {question.id}")
        print(f"Question: {question.question}")
        print("Explanation:", question.explanation or "No explanation provided.")
        print("Answers:")

        # Iterate through each answer related to the question
        for answer in question.answers:
            # Mark the right answer with an asterisk or another signifier
            right_answer_indicator = "*" if answer.is_right_answer else ""
            print(f" - {answer.answer} {right_answer_indicator}")

        print()  # Print a newline for better separation between questions


def extract_letter(text):
    # Regular expression pattern to match uppercase letters followed by a parenthesis
    pattern = r"\b([A-Z])\)"
    # Find all matches in the text
    matches = re.findall(pattern, text)
    return matches


def get_prompt(question):
    def format_answer_options(answers):
        # Create an enumerated list of answers A), B), C), etc.
        options = [
            "{}) {}".format(chr(65 + i), answer.answer)
            for i, answer in enumerate(answers)
        ]
        return "\n".join(options)

    prompt = f"""
Below I will paste a multiple choice python quiz question followed by the possible answers. 
The question may be a fill in the blank type question where the blank is represented by at 
least 3 underscores ('___'). The answers are enumerated with letters. After the list of answers, 
I will write 'End of answers.' You should then answer the question by giving the letter 
associated with the correct answer(s), each letter formatted with a close parenthesee like this "A)". 
Then I would like you to explain why the answer(s) is 
correct. Do not list any additional answer options or repeat the prompt as part of your response.


QUESTION:
{question.question} 

ANSWERS:
{format_answer_options(question.answers)}

End of answers."""
    return prompt


def get_gpt_response(question):
    prompt = get_prompt(question)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extract the response
    api_response = response.choices[0]["message"]["content"]

    # Here we assume the correct answer(s) and explanation are separated by a space and start after 'The correct answer(s) is/are'
    answer_explanation_split = api_response.split("\n", 1)
    if len(answer_explanation_split) == 2:
        # Parse out the correct answers
        _, explanation = answer_explanation_split
        return explanation
    else:
        print(
            "Could not parse the correct answer(s) and explanation properly from the API response."
        )
    return None


# Function to generate explanations for each question and update the database
def generate_explanations_and_update(session):
    """Currently a one time kind of run to fill the db until/if I decide to expand the program."""
    # Retrieve all questions from the database
    questions = session.query(Question).all()

    # Define a helper function to format the answer options

    for question in questions:
        if question.id < 28:
            continue
        # Construct the prompt
        prompt_text = get_prompt(question)

        api_response = get_gpt_response(prompt_text)

        # Here we assume the correct answer(s) and explanation are separated by a space and start after 'The correct answer(s) is/are'
        answer_explanation_split = api_response.split("\n", 1)
        if len(answer_explanation_split) == 2:
            # Parse out the correct answers
            correct_answers_text, explanation = answer_explanation_split
            # correct_answers = correct_answers_text.split(")")[0]
            correct_answers_letters = extract_letter(correct_answers_text)

            # correct_answer_indices = [
            #     ord(answer.strip("[],")) - ord("A") for answer in correct_answers
            # ]
            # correct_answers_indices = ord(correct_answers) - ord("A")
            correct_answers_indices = [
                ord(x) - ord("A") for x in correct_answers_letters
            ]

            # Set the explanation
            # print(correct_answers_text)
            print(question.question)
            print(explanation)

            question.explanation = explanation

            # # Update the correct answers
            for i, answer in enumerate(question.answers):
                # answer.is_right_answer = i in [correct_answer_indices]
                msg = f"{i} {answer.answer} is {i in correct_answers_indices}"
                print(msg)
                answer.is_right_answer = i in correct_answers_indices
            print()

            # # Commit changes to the database
            session.commit()
        else:
            print(
                "Could not parse the correct answer(s) and explanation properly from the API response."
            )


# Usage:
# generate_explanations_and_update(session, 'your-openai-api-key')


if __name__ == "__main__":
    connection = get_db_connection()
    # generate_explanations_and_update(get_session())
    # print_questions_with_answers(get_session())
    # print(connection)
    # recreate_tables()
    fn = "results.csv"
    process_csv(fn)

    # view_questions()
    # print()
    # session = get_session()
    # User.create_new_user(session, "dave", "lynnedavidjohnson@proton.me", "admin")
    # session.commit()
    # session.close()
