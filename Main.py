import os
from quiz.view.quiz import main
from dotenv import load_dotenv

load_dotenv(os.environ["HOME"] + "/.chatgpt")
load_dotenv()


if __name__ == "__main__":
    email = os.environ.get("MY_USER_EMAIL")
    assert email, "environment variable not set"
    assert os.environ.get("OPEN_API_KEY", "Chatgpt key not set")
    main(email)
