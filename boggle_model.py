import tkinter as tki
from ex12_utils import *

class BoggleModel:

    def __init__(self, board):
        """
        This initializes the information
        :return: None
        """
        self.do_clear()
        self.board = board
        self._cur_word = ""
        self._cur_path = []
        self.words = []
        self.load_words()
        self.score = 0
        self.found_words = ''

    def get_current_word(self):
        """
        This get the current word that choose
        :return: current word
        """
        return self._cur_word

    def letter_clicked(self, row, col):
        """
        This check the letters that clicked
        :return: None
        """
        if check_path(self._cur_path + [(row,col)]):
            self._cur_word += self.board[row][col]
            self._cur_path.append((row, col))
            if self._cur_word in self.words and self._cur_word not in self.found_words:
                self.word_found()

    def load_words(self):
        """
        This load the whole words from the dict
        :return: None
        """
        with open("boggle_dict.txt") as file:
            for line in file:
                self.words.append(line.rstrip())

    def do_clear(self):
        """
        This reset the information
        :return: None
        """
        self._cur_score = 0
        self._cur_word = ""
        self._cur_path = []
        self.found_words = ''

    def _do_clear_word(self):
        """
        This reset the word
        :return: None
        """
        self._cur_word = ""
        self._cur_path = []

    def word_found(self):
        """
        This update the information after word found
        :return: None
        """
        self.score += len(self._cur_path) ** 2
        self.found_words += str(self._cur_word) + ', '
        self._cur_path = []
        self._cur_word = ""

    def get_score(self):
        """
        This get the current score
        :return: score
        """
        return self.score

    def get_found_words(self):
        """
        This get the found words
        :return: found words
        """
        return self.found_words





