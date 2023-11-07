"""Tools to process images of a quiz and extract the quizz from images"""

import logging
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import csv
import re

import cv2

import pytesseract
import os

logger = logging.getLogger(__name__)


class FreelancerQuizOcr:
    questions = []
    question = []

    def __init__(self):
        self.question = []
        self.questions = []
        self.current_image_index = -1
        self.images = []
        self.current_image = None

    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.current_image = self.images[self.current_image_index]
            return self.process_file(self.current_image)
        return None

    def process_file(self, fn):
        try:
            self.question = []
            self.fn = fn
            assert os.path.exists(fn)
            self.img = cv2.imread(fn)
            text = self.ocr_core(self.img)
            final_text = self.interpret_question(text)
        except Exception as e:
            logger.exception(str(e))
        return final_text

        return ""

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
        self.question = [question, real_answers]
        return self.question

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


if __name__ == "__main__":
    dir = "/usr/local/dev/ocr/data/images"
    Q = FreelancerQuizOcr()
    Q.process_directory(dir)
    Q.save_to_csv("results.csv")
