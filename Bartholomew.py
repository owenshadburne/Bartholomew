from distutils.cmd import Command
from tkinter import *
# from playsound import playsound
import tkinter.ttk
import time
import tkinter as tk
import random
import string
import re
import json

frame = tk.Tk()
frame.title("Lord Bartholomew")
frame.geometry('800x950')
frame.config(bg="yellow")

json_file = json.load(open("eng_synonyms.json", "r", encoding="utf-8"))

default_reserved_words = ["the", "a", "to", "an", "it",
                          "for", "and", "nor", "but", "or", "yet", "so",
                          "they", "them", "she", "her", "he", "him", "i",
                          "in", "at", "on", "by", "out"]

def remove_reserved(line, words):
    ret = []
    for l in line:
        if l not in words:
            ret.append(l)

    return ret

def strip(line):
    return line.replace("\n", "").strip().translate(str.maketrans('', '', string.punctuation))

def disable_event():
    pass


def reopen():
    frame.deiconify()
    protestFrame.destroy()
    printInput()

def bar_progress_2():
    plead_button['state'] = tk.DISABLED
    barth_speech['text'] = "Deleting System32..."
    bar['value'] = 0
    tasks = 10
    x = 0
    while (x < tasks):
        time.sleep(1)
        bar['value'] += 10
        x += 1
        protestFrame.update()

    if (x == tasks):
        barth_speech['text'] = "Just kidding, but that's what I'd do if I could."
        plead_button["text"] = "Delete OS"
        plead_button['state'] = tk.NORMAL
        plead_button.configure(command=reopen)

def bar_progress():
    plead_button['state'] = tk.DISABLED
    barth_speech['text'] = "Too bad i'm doing it anyways..."
    tasks = 10
    x = 0
    while (x < tasks):
        time.sleep(1)
        bar['value'] += 10
        x += 1
        protestFrame.update()

    if (x == tasks):
        barth_speech['text'] = "Actually, that sentence was so bad i'm ending this entire computer."
        plead_button["text"] = "NO WHY!"
        plead_button['state'] = tk.NORMAL
        plead_button.configure(command=bar_progress_2)

def protest():
    global bar
    global protestFrame
    global barth_speech
    global plead_button
    protestFrame = tk.Tk()
    protestFrame.title("This is a Virus!!!")
    protestFrame.geometry('400x200')
    protestFrame.protocol("WM_DELETE_WINDOW", disable_event)
    protestFrame.resizable(width=False, height=False)
    frame.withdraw()
    bar = tkinter.ttk.Progressbar(protestFrame, orient=tk.HORIZONTAL, length=300)
    bar.pack(pady=10)
    bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    barth_speech = tk.Label(protestFrame, text="That was so bad that i'm ending myself.")
    barth_speech.pack(pady=50)
    plead_button = tk.Button(protestFrame, text="Please Don't!", command=bar_progress)
    plead_button.pack()

def tryProtest():
    rand = random.randint(1, 20)
    if (rand == 1):
        protest()
    else:
        printInput()

def get_random_word(line: list):
    positions = []
    for x in range(len(line)):
        positions.append(x)

    pos = positions[random.randint(0, len(positions) - 1)]
    random_word = strip(line[pos])
    while random_word not in json_file:
        print("Not " + random_word)
        positions.remove(pos)
        if len(positions) <= 0:
            return None
        pos = positions[random.randint(0, len(positions) - 1)]
        random_word = strip(line[pos])

    return random_word

def printInput():
    sentences = sentencetxt.get(1.0, "end-1c")[0: 100]

    if len(strip(sentences)) == 0:
        return

    line = re.split("[\\s*\n]", sentences)

    while "" in line:
        line.remove("")

    global reserved_words
    reserved_words = reservedtxt.get(1.0, "end-1c").split(', ')

    for x in range(len(reserved_words)):
        reserved_words[x] = strip(reserved_words[x].lower())

    if checkbox_status.get():
        reserved_words += default_reserved_words

    global random_word
    random_word = get_random_word(line)
    if random_word == None:
        answer.config(text="Wow, this sentence is really horrible. I'm just not going to rewrite it.")
    else:
        answer.config(text="Really? You thought using '" + random_word + "' was a good idea?")

    global rewrites

    for i in range(10):
        out = randomize(line.copy())
        show = ""
        for j in out:
            show += j + " "
        rewrites[i].config(text=show)


def ui_setup():
    img = PhotoImage(file="ripped_regal.png")
    bg = tk.Label(frame, image=img)
    bg.photo = img
    bg.place(x=0, y=-20, relwidth=1, relheight=1)
    # canvas1 = Canvas(frame, width = 400, height = 400)
    # canvas1.pack(fill = "both", expand = True)
    # canvas1.create_image(0, 0, image = img, anchor = "nw")

    # Sentences
    labelTop = tk.Label(frame, text="\nInput your sentences here.", bg="lime")
    labelTop.pack()
    global sentencetxt
    sentencetxt = tk.Text(frame, height=10, width=90)
    sentencetxt.pack()

    # Reserve
    labelMid = tk.Label(frame, bg="magenta",
                        text="\nType any words you do not to be changed here.\nExample: the, next, a")
    labelMid.pack()
    global reservedtxt
    reservedtxt = tk.Text(frame, bg="lime", height=5, width=50)
    reservedtxt.pack()
    global checkbox, checkbox_status
    checkbox_status = tk.IntVar()
    checkbox = tk.Checkbutton(frame, text='Include the Default Reserved Words', variable=checkbox_status, onvalue=True,
                              offvalue=False)
    checkbox.pack()

    global slider, slider_value
    slider_value = tk.IntVar()
    slider = tk.Scale(frame, variable=slider_value, from_=0, to=100, orient='horizontal')
    slider.pack()
    text = tk.Label(frame, text="Percent chance of replacing any word")
    text.pack()

    spacer = tk.Label(frame, text="\n")
    spacer.pack()

    # Button
    submitButton = tk.Button(frame, text="Rewrite your sentences", command=tryProtest)
    submitButton.pack()

    # Answer
    global answer
    answer = tk.Label(frame, text="")
    answer.pack()

    global rewrites
    rewrites = []

    for i in range(10):
        rewrites.append(tk.Label(frame, text=""))
        rewrites[i].pack()

    # play_button = Button(frame, text="Play Lord Bartholomew's Theme Song", font=("Helvetica", 12), relief=GROOVE, command=playMetal)
    # play_button.pack()


# Todo - make it keep original capitalization
def randomize(l: list):
    for i in range(len(l)):
        s = strip(l[i]).lower()
        if s == random_word:
            l[i] = json_file[s][random.randint(0, len(json_file[s]) - 1)]
        elif random.random() > slider_value.get() / 100:
            continue
        elif s in json_file and s not in reserved_words:
            l[i] = json_file[s][random.randint(0, len(json_file[s]) - 1)]
    return l


'''
def play():
    playsound('theme_song.mp3', False)

def playMetal():
    playsound('barthy_at_full_power.mp3', False)
'''

ui_setup()
# playsound('theme_song.mp3', False)
frame.mainloop()
