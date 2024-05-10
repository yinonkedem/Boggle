from boggle_GUI import *
from boggle_model import *
import sys
import time
import os
from typing import *

class BoggleController:

    def __init__(self):
        """
        This initialize the boggle game
        :return: None
        """
        self._gui = BoggleGUI()
        self._model = BoggleModel(self._gui._board)

        for row in range(4):
            for col in range(4):
                action = self.create_button_action(row, col)
                self._gui.set_button_command(row, col, action)
        reset_action = self.create_reset_action()
        self._gui.set_button_command(4, 0, reset_action)

    def run(self):
        """
        This start the game the boggle game
        :return: None
        """
        self._gui.run()

    def restart(self):
        """
        This restart the boggle game
        :return: None
        """
        os.execl(sys.executable, sys.executable, *sys.argv)

    def create_reset_action(self):
        """
        This reset the boggle model
        :return: None
        """
        def fun():
            self._model._do_clear_word()
            self._gui.set_display(self._model.get_current_word(),
                                  self._model.get_score(),
                                  self._model.get_found_words())
        return fun

    def create_button_action(self, row, col):
        """
        This create the button action
        :return: None
        """
        def fun():
            self._model.letter_clicked(row, col)
            self._gui.set_display(self._model.get_current_word(),
                                  self._model.get_score(),
                                  self._model.get_found_words())
        return fun

if __name__ == "__main__":
    # if sys.argv[0] == 'boggle.py':
    BoggleController().run()

    """
    1. color buttons in current word
    2. pop-up on timer end (controller)
    """