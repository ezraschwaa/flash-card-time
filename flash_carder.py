import os
import sys
import pickle
import tkinter as tk
import random

tk.TK_SILENCE_DEPRECATION = 1

from definition_finder import equip

#Get list of words
if len(sys.argv):
	filename = "/Users/ezraschwartz/Documents/" + sys.argv[1]
else:
	#not really currently incorporated
	print("Enter full working directory of filename:")
	filename = input()

my_file=open(filename,"r")
content = my_file.read()

content_list = content.split("\n")
my_file.close()

#Give definitions to words and write to file
pkl_name = 'FC_words.pkl'  #come back and make this automatic w/ sys argv
								#i.e. parse at the file extension

if os.path.isfile('FC_words.pkl'):  #need to add condition that if len word list != len pkl we re-make the file (for new words)
	print("skipping for now (todo later)")
else:
	definition_list = equip(content_list)
	
	open_file = open(pkl_name, "wb")
	pickle.dump(definition_list, open_file)
	open_file.close()

open_file = open(pkl_name, "rb")
flash_cards_list = pickle.load(open_file)
open_file.close()

#################################
# 		GUI STUFF               #

#now that a file of definitions exist, we'll call it back
#and use it in our GUI
####################################
fcl = flash_cards_list #for convenience
count = 0
card_num_list = random.sample(range(len(fcl)), len(fcl))

window = tk.Tk()
window.title("Flashcard time baby")

frame_card = tk.Frame()
frame_card_count = tk.Frame() 
frame_button = tk.Frame()

card = tk.Label(
	master = frame_card,
	text=fcl[card_num_list[count]][0],
	foreground = "orange",
	background = "#3E4149",
	width = len(fcl[card_num_list[count]])+75,
	height = 7
	)
card_count = tk.Label(
	master = frame_card_count,
	text='Flashcard '+str(count)+'/'+str(len(fcl)),
	foreground = "white",
	background = "#3E4149",
	width = len(fcl[card_num_list[count]])+75,
	height = 1
	)
answer_button = tk.Button(
	master = frame_button,
    text="Answer",
    width=len(fcl[card_num_list[count]])+15,
    height=1,
    bg="black",
    fg="orange",
    highlightbackground = '#3E4149'
)
next_button = tk.Button(
	master = frame_button,
    text="Next Card",
    width=len(fcl[card_num_list[count]])+15,
    height=1,
    bg="black",
    fg="orange",
    highlightbackground = '#3E4149'
)

card.pack(fill=tk.BOTH, expand=True)
card_count.pack(fill = tk.X, expand = True)
answer_button.pack(fill=tk.X)
next_button.pack(fill=tk.X)

frame_card.pack(fill=tk.BOTH, expand=True)
frame_card_count.pack(fill = tk.X)
frame_button.pack(fill=tk.X)

def handle_answer_click(event):
    #print("Answer button was clicked!")
    if answer_button['text'] == 'Answer':
    	card['text'] = ''
    	for definition in fcl[card_num_list[count]][1]:
    		card['text'] += definition + "\n"
    	
    	answer_button['text'] = 'Hide'
    else:
    	card['text'] = fcl[card_num_list[count]][0]
    	answer_button['text'] = 'Answer'


def handle_next_click(event):
    #print("Next button was clicked!")
    answer_button['text'] = 'Answer'

    global card_num_list
    global count
    count+=1
    card['text']=fcl[card_num_list[count]][0]
    card['width'] = len(fcl[card_num_list[count]])+75
    card_count['text'] ='Flashcard '+str(count)+'/'+str(len(fcl))


answer_button.bind("<Button-1>", handle_answer_click)
answer_button.bind("<space>", handle_answer_click)
next_button.bind("<Button-1>", handle_next_click)
next_button.bind("<Return>", handle_next_click)

window.mainloop()


