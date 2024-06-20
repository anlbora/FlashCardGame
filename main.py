import sys
from PyQt5.QtWidgets import QApplication
from FlashCardGame import FlashCardGame 

def main():
    app = QApplication(sys.argv)
    game = FlashCardGame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
