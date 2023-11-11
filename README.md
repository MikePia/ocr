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

