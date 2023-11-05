"""Tools to process images of a quiz and extract the quizz from images"""

import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import csv
import re
import cv2

import pytesseract
import os


class FreelancerQuizOcr:
    questions = []

    def process_file(self, fn):
        self.fn = fn
        assert os.path.exists(fn)
        self.img = cv2.imread(fn)
        text = self.ocr_core(self.img)
        self.interpret_question(text)

    def interpret_question(self, text):
        lines = text.split("\n")
        question = lines[0]
        answers = lines[1:]
        question = self.cleanText(question)
        real_answers = []
        for answer in answers:
            answer = self.cleanText(answer)
            if answer != "":
                if not answer.startswith("Report"):
                    real_answers.append(answer)
                else:
                    break
        edited_question, edited_answers = self.user_edit(
            question, real_answers, self.fn
        )

        self.questions.append({"question": edited_question, "answers": edited_answers})

        print()

    def cleanText(self, text):
        """Extract alphanumeric text, numbers, underscores, spaces, and hyphens from a str"""
        text = re.sub(r"[^a-zA-Z0-9_\- ]", "", text)
        text = text.strip()
        print(text)
        return text

    def ocr_core(self, img):
        text = pytesseract.image_to_string(img)
        return text

    def get_greyscale(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def remove_noise(self, img):
        return cv2.medianBlur(img, 5)

    # thresholding
    def thresholding(self, img):
        return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Move and rename to q<num>.png all the files in a directory to a new directory.
    def move_files(self, src, dst):
        base_name = "qq"
        for i, file in enumerate(os.listdir(src)):
            os.rename(
                os.path.join(src, file), os.path.join(dst, f"{base_name}{i}'.png'")
            )

    def process_directory(self, directory):
        """Process all image files in a given directory."""
        # List all files in the directory
        for filename in os.listdir(directory):
            # Check if the file is an image (can be enhanced further by checking more image extensions)
            if filename.endswith((".png", ".jpg", ".jpeg")):
                filepath = os.path.join(directory, filename)
                self.process_file(filepath)

    def save_to_csv(self, csv_filename):
        """Save processed results to a CSV file."""
        with open(csv_filename, "w", newline="") as csvfile:
            fieldnames = ["question", "answers"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write each question and its answers to the CSV
            for q in self.questions:
                writer.writerow(
                    {"question": q["question"], "answers": ", ".join(q["answers"])}
                )

    def user_edit(self, question, answers, img_path):
        """
        Display the image, extracted question, and answers to the user and allow them to edit.
        Returns the edited question and answers.
        """

        def on_save():
            edited_question.set(question_entry.get())
            edited_answers[:] = [ans_entry.get() for ans_entry in answer_entries]
            root.destroy()

        root = tk.Tk()
        root.title("Edit Question & Answers")

        # Display image
        img = Image.open(img_path)
        img = img.resize((600, 400))  # Resize for display purposes. Adjust as needed.
        img_photo = ImageTk.PhotoImage(img)

        canvas = Canvas(root, width=600, height=400)
        canvas.pack(pady=10)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_photo)

        tk.Label(root, text="Question:").pack(pady=(20, 10))
        question_entry = tk.Entry(root, width=70)
        question_entry.pack(pady=10)
        question_entry.insert(0, question)

        tk.Label(root, text="Answers:").pack(pady=20)
        answer_entries = []
        for answer in answers:
            ans_entry = tk.Entry(root, width=70)
            ans_entry.pack(pady=5)
            ans_entry.insert(0, answer)
            answer_entries.append(ans_entry)

        save_btn = tk.Button(root, text="Save", command=on_save)
        save_btn.pack(pady=20)

        edited_question = tk.StringVar(value=question)
        edited_answers = answers.copy()

        root.mainloop()

        return edited_question.get(), edited_answers


if __name__ == "__main__":
    dir = "/usr/local/dev/ocr/data/images"
    Q = FreelancerQuizOcr()
    Q.process_directory(dir)
    Q.save_to_csv("results.csv")
