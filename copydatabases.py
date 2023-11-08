import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from quiz.models import Question as q

# from quiz.model import login  # Adjust the import path as necessary

# Define the connection URLs
postgres_url = os.environ.get("DATABASE_URL")
sqlite_url = "sqlite:///mydatabase.db"

# Connect to both databases
engine_postgres = create_engine(postgres_url)
engine_sqlite = create_engine(sqlite_url)

# Create sessions for both databases
SessionPostgres = sessionmaker(bind=engine_postgres)
SessionSQLite = sessionmaker(bind=engine_sqlite)

session_postgres = SessionPostgres()
session_sqlite = SessionSQLite()

# Assuming `Question` and other models are your SQLAlchemy model classes
models = [
    q.Question,
    q.User,
    q.Answer,
    q.QuestionNotes,
]  # Replace `login.User` with your actual model class

# Create tables in the SQLite database based on your models
for model in models:
    model.metadata.create_all(engine_sqlite)

# Copy data for each model
for model in models:
    # Query all data from the model in PostgreSQL
    postgres_data = session_postgres.query(model).all()

    # Insert data into the SQLite database
    for data in postgres_data:
        session_sqlite.merge(data)  # merge() is used to handle duplicate primary keys

# Commit and close the sessions
session_sqlite.commit()
session_postgres.close()
session_sqlite.close()

print("Data transfer complete.")
