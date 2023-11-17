import logging
import re
import csv
import openai
import os

from dotenv import load_dotenv

from quiz.models.Question import (
    Question,
    get_db_connection,
    get_session,
)

logger = logging.getLogger(__name__)

load_dotenv(os.environ["HOME"] + "/.chatgpt")
openai.api_key = os.environ["OPENAI_API_KEY"]


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


def get_prompt(question, subject):
    def format_answer_options(answers):
        # Create an enumerated list of answers A), B), C), etc.
        options = [
            "{}) {}".format(chr(65 + i), answer.answer)
            for i, answer in enumerate(answers)
        ]
        return "\n".join(options)

    prompt = f"""
Below I will paste a multiple choice {subject} quiz question followed by the possible answers.
 The question may be a fill in the blank type question where the blank is represented by at
 least 3 underscores ('___'). The answers are enumerated with letters. After the list of answers,
 I will write 'End of answers.' You should then answer the question by giving the correct response 
 like this: "The answer is ____". Do not include the enumerated letter to refer to any of the answers.
 For example, say "The correct answer is all of these", instead of "The correct answer is A) all of these."
 Then I would like you to explain why the answer(s) is
 correct. Do not list any additional answer options or repeat the prompt as part of your response.


QUESTION:
{question.question}

ANSWERS:
{format_answer_options(question.answers)}

End of answers."""
    return prompt


def get_gpt_response(question, subject="python"):
    prompt = get_prompt(question, subject)
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
    return api_response

    # # Here we assume the correct answer(s) and explanation are separated by a space and start after 'The correct answer(s) is/are'
    # answer_explanation_split = api_response.split("\n", 1)
    # if len(answer_explanation_split) == 2:
    #     # Parse out the correct answers
    #     _, explanation = answer_explanation_split
    #     return explanation
    # else:
    #     print(
    #         "Could not parse the correct answer(s) and explanation properly from the API response. Press CTRL R to try again."
    #     )
    # return "Could not parse the correct answer(s) and explanation properly from the API response. Press CTRL R to try again."


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
