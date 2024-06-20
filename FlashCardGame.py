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
        self.hint_index = 0

    def load_flashcards(self):
        try:
            with open('flashcards.json', 'r', encoding='utf-8') as file:
                self.flashcards = json.load(file)
        except UnicodeDecodeError as e:
            print("Error reading JSON file: ", e)
            sys.exit(1)

    def initUI(self):
        self.setWindowTitle('Flash Card Game')

        # Set the overall background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2C3E50"))
        self.setPalette(palette)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Top layout (Score and Category Selection)
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

        # Middle layout (Question Panel)
        middle_layout = QVBoxLayout()

        self.question_label = QLabel('Question')
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setFont(QFont('Verdana', 24, QFont.Bold))
        self.question_label.setStyleSheet("background-color: white; color: black; border-radius: 10px; padding: 10px;")
        self.question_label.setMinimumHeight(200)

        middle_layout.addWidget(self.question_label)
        main_layout.addLayout(middle_layout)

        # Hint and Answer input layout
        hint_answer_layout = QVBoxLayout()

        self.hint_info_label = QLabel('Every Show Hint click, it will only open one letter. After two hints, word will be count as wrong.')
        self.hint_info_label.setAlignment(Qt.AlignCenter)
        self.hint_info_label.setFont(QFont('Verdana', 12))
        self.hint_info_label.setStyleSheet("color: #ECF0F1;") 

        hint_answer_layout.addWidget(self.hint_info_label)

        hint_button_layout = QHBoxLayout()

        self.hint_button = QPushButton('Show Hint')
        self.hint_button.setFont(QFont('Verdana', 16))
        self.hint_button.setStyleSheet("background-color: #F39C12; color: #ECF0F1; border-radius: 10px; padding: 10px;")
        self.hint_button.clicked.connect(self.show_hint)

        self.pass_button = QPushButton('Pass')
        self.pass_button.setFont(QFont('Verdana', 16))
        self.pass_button.setStyleSheet("background-color: #E74C3C; color: #ECF0F1; border-radius: 10px; padding: 10px;")
        self.pass_button.clicked.connect(self.pass_card)

        hint_button_layout.addWidget(self.hint_button)
        hint_button_layout.addWidget(self.pass_button)
        hint_answer_layout.addLayout(hint_button_layout)

        answer_layout = QHBoxLayout()

        self.hint_input = QLineEdit()
        self.hint_input.setFont(QFont('Verdana', 16))
        self.hint_input.setStyleSheet("padding: 5px; border-radius: 10px;")
        self.hint_input.setPlaceholderText('Answer')

        self.submit_button = QPushButton('Submit')
        self.submit_button.setFont(QFont('Verdana', 16))
        self.submit_button.setStyleSheet("background-color: #3498DB; color: #ECF0F1; border-radius: 10px; padding: 10px;")
        self.submit_button.clicked.connect(self.check_answer)

        answer_layout.addWidget(self.hint_input)
        answer_layout.addWidget(self.submit_button)

        hint_answer_layout.addLayout(answer_layout)
        main_layout.addLayout(hint_answer_layout)

        # Bottom layout (Statistics)
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
            self.hint_index = 0
        else:
            self.question_label.setText('Game Over!')
            self.hint_input.setDisabled(True)
            self.submit_button.setDisabled(True)
            self.hint_button.setDisabled(True)
            self.pass_button.setDisabled(True)

    def show_hint(self):
        if self.current_flashcards:
            flashcard = self.current_flashcards[self.current_index]
            correct_answer = flashcard['answer'] 
            
            if self.hint_input.text() == '' or len(self.hint_input.text()) != len(correct_answer):
                hint = '*' * len(correct_answer)
            else:
                hint = self.hint_input.text()


            unrevealed_positions = [i for i in range(len(correct_answer)) if hint[i] == '*']
            if unrevealed_positions:

                reveal_index = random.choice(unrevealed_positions)
                
  
                hint = ''.join(
                    correct_answer[i] if i == reveal_index or hint[i] != '*' else '*'
                    for i in range(len(correct_answer))
                )
                
    
                self.hint_input.setText(hint)
                self.hint_index += 1

    def check_answer(self):
        answer = self.hint_input.text().strip().replace('*', '')
        flashcard = self.current_flashcards[self.current_index]
        correct_answer = flashcard['answer']  

        if answer.lower() == correct_answer.lower():
            if self.hint_index == 0:
                self.score += 10  
            elif self.hint_index == 1:
                self.score += 5 
            self.cards_correct += 1
            self.question_label.setStyleSheet("background-color: green; color: white; border-radius: 10px; padding: 10px;")
            self.current_flashcards.pop(self.current_index) 
            if self.current_flashcards:
                self.current_index = self.current_index % len(self.current_flashcards)  
        else:
            self.cards_wrong += 1
            self.question_label.setText(f'Correct Answer: {correct_answer}')
            self.question_label.setStyleSheet("background-color: red; color: white; border-radius: 10px; padding: 10px;")
            

            if self.hint_index > 1:
                self.seen_flashcards.append(flashcard)
                self.current_flashcards.pop(self.current_index)
            else:
                
                self.current_index = self.current_index % len(self.current_flashcards)

        self.update_score()
        QTimer.singleShot(2000, self.next_card)  

    def pass_card(self):
        if self.current_flashcards:
            self.seen_flashcards.append(self.current_flashcards.pop(self.current_index))
            if self.current_flashcards:
                self.current_index = self.current_index % len(self.current_flashcards) 
            self.update_score()
            self.next_card(randomize=True)

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
            self.hint_input.clear()

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
