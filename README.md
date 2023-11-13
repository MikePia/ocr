# A program to create and run quizes.
## Features
* GUI Written in Pyside6
* Explanation of answers dynamiclly retrieved from openai and stored to your database (requires openai token)
* Notes on each question stored and displayed for each user.
* Utility to create new question
* Will store data in any database supported by SqlAlchemy. Uses sqlite database file by default
  * To use Postgres for example write something like this in .env
```DATABASE_URL=postgresql://postgres:somepassword@localhost:5432/quiz```
This will connect to username postgres on the localhost

![Alt text](./images/quizzer.png)

Create new questions using this tool
![Alt text](./images/create_question.png)
* Extract questions from images, create them from scratch, load questions from csv.


### If there is any interest in this app
* To reporting problems/bugs/requests create an issue here:
[github issue for quizzer](https://github.com/MikePia/quizzer/issues)
# Install
And I use the term loosley :smile:

Python is required
Recommend you use a virtual environment. 
Open a terminal and navigate to your intended project directory

### Mandatory
```bash
mkdir quizzer
cd quizzer
git clone https://github.com/MikePia/quizzer.git .
```

### Optional virtual environment
```bash
python3 python -m venv .venv_quizzer
# In Linux / bash
source .venv_quizzer/bin/activate
# In cmd.exe
venv_quizzer\Scripts\activate.bat
# In PowerShell
venv_quizzer\Scripts\Activate.ps1
```
### Mandatory
```
pip install -r requirements.txt

 ```



Create a file named ```.env``` in the project directory place the following in it

```txt
OPEN_API_KEY=<your-openai-api-key>
DATABASE_URL="sqlite:///mydatabase.db"
# or give a full path to where ever you want to place your database like
DATABASE_URL="sqlite:////user/local/utility/quizzer2/mydatabase.db"

# Run the program
python Main.py
```


# Why ... ?
I created this tool to sudy and pass a few Freelancer Skill Tests. Currently the tests are 40 questions in 15 minutes. That's 22 seconds a question. The process is pretty effective. Here is how I use it.
* Take the exam
* Do screenshots of each question by hitting the print screen command as I take the test. The OCR works best if the image does not have extra space. Just copy the question and the answers as tightly as possible
* Start quizzer and choose Create Question
  * Choose process directory and load the images
  * Run through each question fixing up all the OCR oddities.
* Run the questions  
  * (use arrow keys ***<--, -->*** to navigate, ***Ctrl K*** to set the right answer and ***Enter*** to submit and get GPT explanation)
  * Answer the questions 
  * Submit the questions to acitvate GPT explanation. The explanations are usually great snippits that make remembering the material a breeze.
  * Save any notes, especially for ambiguous answers from GPT
  * Set the Correct answer (Ctrl K)
* Re-run the questions till I can complete them without a mistake
* Re take the Freelancer exam, doing screenshots only of questions I haven't seen
* Ace the Freelancer exam :smile:
