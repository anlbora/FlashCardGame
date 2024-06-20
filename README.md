# Flash Card Game

This Flash Card Game is designed to help users enhance their vocabulary by matching English words with their Turkish translations. It's built using Python and the PyQt5 library, offering an interactive and visually appealing interface.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Game Categories](#game-categories)
- [User Interface](#user-interface)
- [How to Play](#how-to-play)
- [File Structure](#file-structure)

## Overview

The Flash Card Game presents words in English and challenges the user to provide the corresponding Turkish translation. It's an engaging way to learn and test your language skills across various categories.

## Features

- **Multiple Categories**: Choose from a variety of categories including Animals, Colors, Occupations, Sports, and Furniture.
- **Score Tracking**: Keep track of your score and see how well you are doing.
- **Progress Tracking**: Monitor the percentage of correct answers and the number of remaining cards.
- **Pass Option**: Skip difficult cards and revisit them later.
- **Randomized Flash Cards**: Cards are shown in random order to enhance learning and avoid predictability.

## Game Categories

The game includes the following categories, each with a set of 25 entries:
- **Animals**: English and Turkish names of common animals.
- **Colors**: English and Turkish names of various colors.
- **Occupations**: Different job titles and their Turkish translations.
- **Sports**: Names of sports and their Turkish equivalents.
- **Furniture**: Common furniture items and their names in Turkish.

## User Interface

### Main Components:

- **Category Selection**: A dropdown menu to select the category of words you want to practice.
- **Flash Card Display**: Shows the English word, which you need to translate to Turkish.
- **Input Box**: Type your answer here.
- **Buttons**:
  - **Submit**: Check your answer.
  - **Pass**: Skip the current card and revisit it later.
- **Score and Statistics**: Displays your score, number of correct and wrong answers, and the percentage of correctness.

### UI Design:
The game features a clean and user-friendly design with a responsive layout. It is built using PyQt5, ensuring compatibility across different platforms.

## How to Play

1. **Launch the Game**:
    - Start the game by running the `main.py` script in your terminal or Python environment.

2. **Choose a Category**:
    - Use the dropdown menu to select a category you want to practice.

3. **Translate the Word**:
    - A flash card will display an English word. Type its Turkish translation in the input box.

4. **Submit Your Answer**:
    - Click the "Submit" button to check your answer.
    - If your answer is correct, the card turns green, and your score increases.
    - If your answer is incorrect, the correct translation is shown, and the card turns red.

5. **Pass if Needed**:
    - Use the "Pass" button to skip difficult words. They will be shown again later.

6. **Track Your Progress**:
    - Keep an eye on your score and the percentage of correct answers.

7. **Complete the Game**:
    - The game ends when all cards in the selected category are answered correctly.

## File Structure

- `main.py`: The main script that runs the game. It includes the game logic and UI setup.
- `flashcards.json`: A JSON file containing the flash card data for each category.
- `README.md`: The readme file providing an overview and instructions for the game.

### Example Code Snippet

Here's a brief look at how the game logic is implemented in `main.py`:

```python
import sys
import json
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette

class FlashCardGame(QWidget):
    def __init__(self):
        super().__init__()
        self.load_flashcards()
        self.initUI()
        self.current_category = None
        self.current_flashcards = []
        self.seen_flashcards = []
        self.current_index = -1
        self.score = 0
        self.cards_correct = 0
        self.cards_wrong = 0

    def load_flashcards(self):
        try:
            with open('flashcards.json', 'r', encoding='utf-8') as file:
                self.flashcards = json.load(file)
        except Exception as e:
            print("Error reading JSON file: ", e)
            sys.exit(1)

    def initUI(self):
        self.setWindowTitle('Flash Card Game')
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2C3E50"))  # Dark blue background
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        top_layout = QHBoxLayout()
        self.score_label = QLabel('SCORE: 000')
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont('Verdana', 24, QFont.Bold))
        self.score_label.setStyleSheet("color: #ECF0F1;")
        self.category_combobox = QComboBox()
        self.category_combobox.setFont(QFont('Verdana', 16))
        self.category_combobox.addItem('Select Category')
        self.category_combobox.addItems(self.flashcards.keys())
        self.category_combobox.currentIndexChanged.connect(self.select_category)

        top_layout.addWidget(self.score_label)
        top_layout.addWidget(self.category_combobox)
        main_layout.addLayout(top_layout)

        middle_layout = QVBoxLayout()
        self.question_label = QLabel('Question')
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setFont(QFont('Verdana', 24, QFont.Bold))
        self.question_label.setStyleSheet("background-color: white; color: black; border-radius: 10px; padding: 10px;")
        self.question_label.setMinimumHeight(200)

        middle_layout.addWidget(self.question_label)
        main_layout.addLayout(middle_layout)

        answer_layout = QVBoxLayout()
        self.answer_input = QLineEdit()
        self.answer_input.setFont(QFont('Verdana', 16))
        self.answer_input.setStyleSheet("padding: 5px; border-radius: 10px;")
        self.answer_input.setPlaceholderText('Answer')
        self.submit_button = QPushButton('Submit')
        self.submit_button.setFont(QFont('Verdana', 16))
        self.submit_button.setStyleSheet("background-color: #3498DB; color: #ECF0F1; border-radius: 10px; padding: 10px;")
        self.submit_button.clicked.connect(self.check_answer)

        answer_layout.addWidget(self.answer_input)
        answer_layout.addWidget(self.submit_button)
        main_layout.addLayout(answer_layout)

        bottom_layout = QHBoxLayout()
        self.cards_remaining_label = QLabel('0 Cards Remaining')
        self.cards_remaining_label.setFont(QFont('Verdana', 14))
        self.cards_remaining_label.setStyleSheet("color: #ECF0F1;")
        self.cards_correct_label = QLabel('0 Cards Correct')
        self.cards_correct_label.setFont(QFont('Verdana', 14))
        self.cards_correct_label.setStyleSheet("color: #ECF0F1;")
        self.cards_wrong_label = QLabel('0 Cards Wrong')
        self.cards_wrong_label.setFont(QFont('Verdana', 14))
        self.cards_wrong_label.setStyleSheet("color: #ECF0F1;")
        self.percent_correct_label = QLabel('%0 Correct')
        self.percent_correct_label.setFont(QFont('Verdana', 14))
        self.percent_correct_label.setStyleSheet("color: #ECF0F1;")

        bottom_layout.addWidget(self.cards_remaining_label)
        bottom_layout.addWidget(self.cards_correct_label)
        bottom_layout.addWidget(self.cards_wrong_label)
        bottom_layout.addWidget(self.percent_correct_label)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def select_category(self):
        category = self.category_combobox.currentText()
        if category != 'Select Category':
            self.current_category = category
            self.current_flashcards = self.flashcards[category][:]
            self.seen_flashcards = []
            self.score = 0
            self.cards_correct = 0
            self.cards_wrong = 0
            self.update_score()
            self.next_card(randomize=True)

    def update_question(self):
        if self.current_flashcards:
            flashcard = self.current_flashcards[self.current_index]
            question = flashcard['question']
            self.question_label.setText(question)
            self.question_label.setStyleSheet("background-color: white; color: black; border-radius: 10px; padding: 10px;")
            self.cards_remaining_label.setText(f'{len(self.current_flashcards)} Cards Remaining')
        else:
            self.question_label.setText('Game Over!')
            self.answer_input.setDisabled(True)
            self.submit_button.setDisabled(True)

    def check_answer(self):
        answer = self.answer_input.text().strip()
        flashcard = self.current_flashcards[self.current_index]
        correct_answer = flashcard['answer']

        if answer.lower() == correct_answer.lower():
            self.score += 10
            self.cards_correct += 1
            self.question_label.setStyleSheet("background-color: green; color: white; border-radius: 10px; padding: 10px;")
            self.current_flashcards.pop(self.current_index)
            if self.current_flashcards:
                self.current_index = self.current_index % len(self.current_flashcards)
        else:
            self.cards_wrong += 1
            self.question_label.setText(f'Correct Answer: {correct_answer}')
            self.question_label.setStyleSheet("background-color: red; color: white; border-radius: 10px; padding: 10px;")

        self.update_score()
        QTimer.singleShot(2000, self.next_card)

    def next_card(self, randomize=False):
        if not self.current_flashcards and self.seen_flashcards:
            self.current_flashcards = self.seen_flashcards[:]
            self.seen_flashcards = []
        if self.current_flashcards:
            if randomize:
                self.current_index = random.randint(0, len(self.current_flashcards) - 1)
            else:
                self.current_index += 1
                if self.current_index >= len(self.current_flashcards):
                    self.current_index = 0
            self.update_question()
            self.answer_input.clear()

    def update_score(self):
        self.score_label.setText(f'SCORE: {self.score:03}')
        self.cards_correct_label.setText(f'{self.cards_correct} Cards Correct')
        self.cards_wrong_label.setText(f'{self.cards_wrong} Cards Wrong')
        total_attempts = self.cards_correct + self.cards_wrong
        percent_correct = (self.cards_correct / total_attempts) * 100 if total_attempts > 0 else 0
        self.percent_correct_label.setText(f'%{percent_correct:.0f} Correct')
        self.cards_remaining_label.setText(f'{len(self.current_flashcards)} Cards Remaining')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = FlashCardGame()
    sys.exit(app.exec_())




```
```
{
    "Animals": [
        {"question": "Cat", "answer": "Kedi"},
        {"question": "Dog", "answer": "Köpek"},
        ...
    ],
    "Colors": [
        {"question": "Red", "answer": "Kırmızı"},
        {"question": "Blue", "answer": "Mavi"},
        ...
    ],
    "Occupations": [
        {"question": "Doctor", "answer": "Doktor"},
        {"question": "Teacher", "answer": "Öğretmen"},
        ...
    ],
    "Sports": [
        {"question": "Soccer", "answer": "Futbol"},
        {"question": "Basketball", "answer": "Basketbol"},
        ...
    ],
    "Furniture": [
        {"question": "Chair", "answer": "Sandalye"},
        {"question": "Table", "answer": "Masa"},
        ...
    ]
}
```
