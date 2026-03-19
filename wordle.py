### UI ###

import customtkinter as ctk

class WordleWindow(ctk.CTk):
    def __init__(self, on_submit_callback):
        super().__init__()
        self.title("Wordle UI Bridge")
        self.geometry("400x600")
        ctk.set_appearance_mode("dark")

        # This is the function from your second script we will call on Enter
        self.on_submit_callback = on_submit_callback

        self.rows = []
        self.current_row = 0
        self.current_guess = "" # Internal tracker for the active string
        self.colors = {2: "#538d4e", 1: "#b59f3b", 0: "#3a3a3c"}

        # Build Grid
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(pady=50)

        for r in range(6):
            row_cells = []  # Create the temporary list for this row
            for c in range(5):      
                # 1. Create the Frame (The Border/Box)
                cell_container = ctk.CTkFrame(
                    self.grid_frame, 
                    width=55, 
                    height=55, 
                    border_width=2,
                    border_color="#3a3a3c",
                    fg_color="transparent"
                )
                cell_container.grid(row=r, column=c, padx=3, pady=3)
                cell_container.grid_propagate(False)

                # 2. Create the Label (The Letter)
                cell_label = ctk.CTkLabel(
                    cell_container, 
                    text="", 
                    font=("Helvetica", 28, "bold")
                )
                cell_label.place(relx=0.5, rely=0.5, anchor="center")

                # 3. Append the FRAME to the row list
                row_cells.append(cell_container)

            # 4. Append the completed row to the main rows list
            self.rows.append(row_cells)

        self.status_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.status_label.pack(pady=20)

        # Handle Keypresses
        self.bind("<Key>", self._handle_keypress)

                # Inside __init__
        self.restart_button = ctk.CTkButton(
        self, 
        text="Play Again", 
        command=self.reset_game,
        fg_color="#538d4e", 
        hover_color="#3e663a"
        )
        # We don't pack it yet; we wait for Game Over.

    def _handle_keypress(self, event):
        key = event.char
        keysym = event.keysym

        if keysym == "BackSpace":
            if len(self.current_guess) > 0:
                self.current_guess = self.current_guess[:-1]
                self.show_message("") 
        
        elif keysym == "Return":
            if len(self.current_guess) == 5:
                # 1. Send to logic (which calls color_row)
                self.on_submit_callback(self.current_guess.lower())
                
                # 2. Move to the next row in the UI
                self.current_row += 1
                
                # 3. Reset the string for the NEW row
                self.current_guess = ""
                
                # 4. Optional: Check if game is over
                if self.current_row > 5:
                    self.show_game_over("Game Over")
            else:
                self.show_message("Word too short")
            return 

        elif len(self.current_guess) < 5 and key.isalpha():
            # Ensure only single letters are added (ignores modifier keys)
            if len(key) == 1: 
                self.current_guess += key.upper()

        self.update_typing(self.current_guess)

    def show_game_over(self, message):
        self.status_label.configure(text=message)
        self.restart_button.pack(pady=10)
        # Optional: Unbind keys so the user can't keep typing
        self.unbind("<Key>")

    def update_typing(self, current_guess):
        for i in range(5):
                # 1. Get the Frame
                cell_frame = self.rows[self.current_row][i]

                # 2. Get the Label inside the frame
                cell_label = cell_frame.winfo_children()[0]

                # 3. Update the label text
                if i < len(current_guess):
                        cell_label.configure(text=current_guess[i].upper())
                else:
                        cell_label.configure(text="")

    def color_row(self, scores):
        for i, score in enumerate(scores):
                # This is now the Frame
                cell_frame = self.rows[self.current_row][i]

                # This gets the Label inside the frame
                cell_label = cell_frame.winfo_children()[0]

                # Update the Frame (Background and Border)
                new_color = self.colors.get(score, "#3a3a3c")
                cell_frame.configure(
                fg_color=new_color,
                border_width=0  # This works now!
                )

                # Update the Label (Text color)
                cell_label.configure(text_color="white")

    def show_message(self, message, color="white"):
        self.status_label.configure(text=message, text_color=color)

    def reset_grid(self):
        self.current_row = 0
        self.current_guess = ""
        for row in self.rows:
            for cell in row:
                cell.configure(text="", fg_color="transparent", border_width=2)

    def run(self):
        """Starts the UI loop."""
        self.mainloop()

    def reset_game(self):
        # 1. Reset variables
        self.current_row = 0
        self.current_guess = ""
        self.status_label.configure(text="")
        
        # 2. Hide the button again
        self.restart_button.pack_forget()
        
        # 3. Clear the UI Grid
        for row in self.rows:
                for cell_frame in row:
                # Reset Frame
                        cell_frame.configure(
                                fg_color="transparent", 
                                border_width=2, 
                                border_color="#3a3a3c"
                        )
                        # Reset Label
                        cell_label = cell_frame.winfo_children()[0]
                        cell_label.configure(text="")

        # 4. Re-bind keys (if you unbound them)
        self.bind("<Key>", self._handle_keypress)
        pick_word()


### MY Logic ###
import os, sys
import pandas as pd
import random as rand


app = ''

target = ''

class colours:
        yellow = '\033[93m'
        green = '\033[32m'
        endc = '\033[0m'

blank_alpha = 'abcdefghijklmnopqrstuvwxyz'
current_alphabet = blank_alpha

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

dict = pd.read_csv(resource_path('words_len_5.csv'))


def run_game():
        global target, app
        rounds = 6
        pick_word()
        app = WordleWindow(on_submit_callback=on_submit)
        app.mainloop()

# def game(rounds: int, word: str):
#         alphabet = blank_alpha

#         guesses = []
#         while (rounds > 0):
#                 print(f'Guesses remaining: {rounds}\n')
#                 outval, alphabet = round(word, guesses, alphabet)
#                 if outval == 1:
#                         return True
#                 else:
#                         guesses.append(outval)
#                 rounds -= 1

#         print('Failure!')

def pick_word():
        global target
        word_index = rand.randint(0, len(dict) - 1)
        target = str(dict.iloc[word_index].word).lower()
        current_alphabet = blank_alpha


def round(word: str, guesses: list, alpha: str):
        if guesses is not None:
                for g in guesses: # print guess list
                        wordout, alpha, _ = colour_guess(g, word, alpha)
                        print(wordout)

        return guess, alpha

def on_submit(guess: str):
        global target, current_alphabet, app

        if not is_valid_guess(guess):
                app.show_message('Bad guess', color='#ff4b4b')
                return

        strout, current_alphabet, ls = colour_guess(guess, target, current_alphabet)

        app.color_row(ls)
        print(f"Terminal view: {strout} | Letters left: {current_alphabet}")


        if all(s == 2 for s in ls):
                app.show_message('GENIUS!', color='#538d4e')
                app.unbind('<Key>')
        elif app.current_row >= 6:
                app.show_message('Game Over', color='#ff4b4b')

def colour_guess(guess: str, word: str, alpha: str=''):
        ls = [0, 0, 0, 0, 0]
        strout = ''
        for i in range(len(guess)): # needs better colouring for maybes if already has the green: if all occurances of letter are marked green, don't mark that letter as yellow
                if (guess[i] == word[i]):
                        strout += (colours.green + guess[i] + colours.endc)
                        ls[i] = 2
                elif (guess[i] in word):
                        strout += (colours.yellow + guess[i] + colours.endc)
                        ls[i] = 1
                else:
                        strout += (guess[i])
                        ls[i] = 0
                        if alpha != '':
                                alpha = alpha.replace(guess[i], '')

        return strout, alpha, ls

def is_valid_guess(guess: str):
        if len(guess) != 5: # swap for function that allows variable length
                print('Incorrect length.')
                return False

        if not guess.isalpha():
                print('Not alphabetic characters.')
                return False

        # if guess not in dict.word:
        #         print('Not in dictionary.')
        #         return False

        return True

run_game()
