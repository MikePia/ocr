# A program to create and run quizes.
## Features
* GUI Written in Pyside6
* Explanation of answers dynamiclly retrieved from openai and stored to your database
* Notes on each question stored and displayed for each user.
* Utility to create new question
* Will store data in a sqlite database file by default
* Uses Sqlalchemy, so you can use most any database by supplying the connection string
  * To use Postgres for example write something like this in .env
```DATABASE_URL=postgresql://postgres:somepassword@localhost:5432/quiz```
This will connect to username postgres on the localhost

![Alt text](./images/quizzer.png)

Create new questions using this tool
![Alt text](./images/create_question.png)
* Uses OCR to extract a quiz question from an image and places the data in a form
* Use the same tool without an image to create questions

