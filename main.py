from tkinter import *
from random import choice
import pandas


BACKGROUND_COLOR = "#B1DDC6"
FRENCH = "French"
ENGLISH = "English"
current_card = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def correct():
    to_learn.remove(current_card)
    update_words()
    new_card()


def update_words():
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)


def new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    original_word = current_card["French"]

    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(language, text=FRENCH, fill="black")
    canvas.itemconfig(word, text=original_word, fill="black")

    flip_timer = window.after(3000, flip_card)


def flip_card():
    translated_word = current_card["English"]
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(language, text=ENGLISH, fill="white")
    canvas.itemconfig(word, text=translated_word, fill="white")


# Window set-up

window = Tk()

window.title("Flashcard")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)


# Images

card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")

right_button_image = PhotoImage(file="images/right.png")
wrong_button_image = PhotoImage(file="images/wrong.png")

# Arranging visual elements

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(800 / 2, 526 / 2, image=card_front_img)
language = canvas.create_text(800 / 2, 526 / 2 - 100, fill="black", font=("Calibri", 25, "italic"))
word = canvas.create_text(800 / 2, 526 / 2, fill="black", font=("Calibri", 45, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=new_card)
wrong_button.grid(row=1, column=0)

right_button = Button(image=right_button_image, highlightthickness=0, command=correct)
right_button.grid(row=1, column=1)

# Running the program

new_card()

window.mainloop()
