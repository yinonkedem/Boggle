import tkinter as tki
from tkinter import messagebox
import boggle
from boggle_board_randomizer import *
from boggle import *
import time
import textwrap
from typing import *

BUTTON_HOVER_COLOR = 'grey'
REGULAR_COLOR = 'lightgray'
BUTTON_PRESSED_COLOR = 'green'
BUTTON_ACTIVE_COLOR = 'slateblue'
BUTTON_STAYLE = {"font": ('Courier', 30), "borderwidth": 1, "relief": tki.RAISED, "bg": REGULAR_COLOR, "activebackground": BUTTON_ACTIVE_COLOR}
GAME_TIME = 180

class BoggleGUI:

    def __init__(self):
        """
        This initialize the boggle visualization
        :return: None
        """
        root = tki.Tk()
        root.title("Boggle Game")
        root.resizable(False, False)
        board = randomize_board(dice_list=LETTERS)
        self._buttons = [[]]
        self.init_button_matrix()
        self._board = board
        self._main_window = root

        self._outer_frame = tki.Frame(root, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR, highlightthickness=5)
        self._outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._my_words_label = tki.Label(self._outer_frame, font=("Courier", 13), bg=REGULAR_COLOR,
                                         width=30, relief="sunken", anchor="n")
        self._my_words_label.pack(side=tki.RIGHT, fill=tki.BOTH, expand=True)

        self._timer_label = tki.Label(self._outer_frame, font=("Courier", 30), bg=REGULAR_COLOR,
                                      width=23, relief="sunken")
        self._timer_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._score_label = tki.Label(self._outer_frame, font=("Courier", 30), bg=REGULAR_COLOR,
                                      width=23, relief="sunken")
        self._score_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._word_label = tki.Label(self._outer_frame, font=("Courier", 30), bg=REGULAR_COLOR,
                                     width=23, relief="sunken")
        self._word_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._lower_frame = tki.Frame(self._outer_frame)
        self._lower_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._create_bottons_in_lower_frame()
        self._create_reset_button()

    def run(self):
        """
        This start the game the boggle gui
        :return: None
        """
        self._main_window.withdraw()
        start_q = messagebox.askquestion("start the game", "ready?")
        if start_q =='yes':
            self._main_window.deiconify()
            self.set_display("choose words", 0, '')
            self.countdown(GAME_TIME)
            self._main_window.mainloop()
        else:
            self._main_window.quit()

    def set_display(self, cur_word: str, score, words_found):
        """
        This set the gui display
        :return: None
        """
        text_my_words = textwrap.fill(words_found, width=30)
        self._word_label["text"] = cur_word
        self._my_words_label["text"] = "words bank:\n" + text_my_words
        self._score_label["text"] = "score: " + str(score)

    def set_button_command(self, row, col, cmd: Callable[[], None]):
        """
        This set the button command
        :return: None
        """
        self._buttons[row][col].configure(command=cmd)

    def _create_bottons_in_lower_frame(self):
        """
        This create the buttons
        :return: None
        """
        for i in range(4):
            tki.Grid.columnconfigure(self._lower_frame, i, weight=1)

        for i in range(4):
            tki.Grid.rowconfigure(self._lower_frame, i, weight=1)


        for row in range(4):
            for col in range(4):
                self._make_button(row,col)

    def _create_reset_button(self):
        """
        This create the reset button
        :return: None
        """
        tki.Grid.columnconfigure(self._lower_frame, 0, weight=1)
        tki.Grid.rowconfigure(self._lower_frame, 4, weight=1)

        button = tki.Button(self._lower_frame, text="Reset Word", **BUTTON_STAYLE)
        button.grid(row=4, column=0, rowspan=1, columnspan=4, sticky=tki.NSEW)
        self._buttons[4][0] = button

        def _on_enter(event: Any):
            button["background"] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any):
            button["background"] = REGULAR_COLOR

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)

        return button

    def _make_button(self, row: int, col: int, rowspan: int = 1, colspan: int = 1):
        """
        This change the button while the game run proper to the situation
        :return: None
        """
        button = tki.Button(self._lower_frame, text=self._board[row][col], **BUTTON_STAYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=tki.NSEW)
        self._buttons[row][col] = button

        def _on_enter(event: Any):
            button["background"] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any):
            button["background"] = REGULAR_COLOR

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)

        return button

    def init_button_matrix(self):
        """
        This init the whole buttons
        :return: None
        """
        for row in range(4):
            self._buttons.append([])
            for col in range(4):
                self._buttons[row].append(None)
        self._buttons.append([])
        self._buttons[4].append(None)

    def countdown(self, count):
        """
        This create the timer
        :return: None
        """
        # change text in label
        self._timer_label['text'] = str(count) + " seconds"

        if count > 0:
            # call countdown again after 1000ms (1s)
            self._main_window.after(1000, self.countdown, count - 1)
        if count == 0:
            self._timer_label['text'] = "Time's Up!"
            play_again = messagebox.askquestion("paly again", "do you want to play again?")
            if play_again == 'yes':
                boggle.BoggleController.restart(boggle)
            if play_again == 'no':
                self._main_window.quit()