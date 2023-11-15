import os
from quiz.view.quiz import main
from dotenv import load_dotenv

load_dotenv(os.environ["HOME"] + "/.quizzer_rc")


if __name__ == "__main__":
    assert os.environ.get("OPENAI_API_KEY", "Chatgpt key not set")
    main()
