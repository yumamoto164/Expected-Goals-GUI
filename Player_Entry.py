import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date
from joblib import load
from tkinter import *
import tkinter.font as tkFont
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import ginput
from matplotlib.patches import Arc
from matplotlib.widgets import Cursor
from functools import partial
from Shot import Player, Shot
from mplsoccer.pitch import Pitch

home_number_entries = []
home_player_entries = []
away_number_entries = []
away_player_entries = []

def submit_teams():
    home_list = []
    away_list = []
    home_team = home_entry.get()
    away_team = away_entry.get()
    
    if (home_team == '') or (away_team == ''):
        error_label.config(text="Please fill in the home and away team names to submit.")
        return
    else:
        error_label.config(text='')
    
    for i in range(20):
        if ((home_number_entries[i].get() == '') is not (home_player_entries[i].get() == '')) or ((away_number_entries[i].get() == '') is not (away_player_entries[i].get() == '')):
            error_label.config(text="There is at least one blank entry. Please fill that in to submit.")
            return
        else:
            if (home_number_entries[i].get() != ''):
                new_home_player = Player(home_team, int(home_number_entries[i].get()), home_player_entries[i].get())
                home_list.append(new_home_player)
            
            if (away_number_entries[i].get() != ''):
                new_away_player = Player(away_team, int(away_number_entries[i].get()), away_player_entries[i].get())
                away_list.append(new_away_player)
    
    print(home_list[0].getTeam(), home_list[0].getNumber(), home_list[0].getName())
    print(away_list[0].getTeam(), away_list[0].getNumber(), away_list[0].getName())
    

base = Tk()

Grid.rowconfigure(base, 0, weight=1)
Grid.columnconfigure(base, 0, weight=1)

team_label_font = tkFont.Font(family='Helvetica', size=16, weight='bold')
team_entry_font = tkFont.Font(family='Hevetica', size=12)
button_font = tkFont.Font(family='Hevetica', size=12)
reg_font = tkFont.Font(family='Hevetica', size=12)

team_frame = LabelFrame(base, padx=10, pady=5)
team_frame.pack(side=TOP, padx=10, pady=5)

home_label = Label(team_frame, text="Home", font=team_label_font)
away_label = Label(team_frame, text="Away", font=team_label_font)

home_label.grid(row=0, column=0, sticky=N+S+E+W)
away_label.grid(row=0, column=3, sticky=N+S+E+W)

home_name_label = Label(team_frame, text="Enter Home Team: ", font=team_entry_font)
away_name_label = Label(team_frame, text="Enter Away Team: ", font=team_entry_font)
home_entry = Entry(team_frame, width=20)
away_entry = Entry(team_frame, width=20)
home_name_label.grid(row=1, column=0) # sticky=N+S+E+W)
away_name_label.grid(row=1, column=3) #, sticky=N+S+E+W)
home_entry.grid(row=1, column=1, padx=(0,50), ipady=3) #, sticky=N+S+E+W)
away_entry.grid(row=1, column=4, ipady=3) #, sticky=N+S+E+W)

player_entry_frame = LabelFrame(base, padx=5, pady=5)
player_entry_frame.pack(padx=5, pady=5)

number_label = Label(player_entry_frame, text="Number")
number_label2 = Label(player_entry_frame, text="Number")
name_label = Label(player_entry_frame, text="Player Name")
name_label2 = Label(player_entry_frame, text="Player Name")

number_label.grid(row=0, column=0)
name_label.grid(row=0, column=1, padx=(0,10))
number_label2.grid(row=0, column=2)
name_label2.grid(row=0, column=3)

for x in range(20):
    home_numbers = Entry(player_entry_frame, width=5)
    home_players = Entry(player_entry_frame, width=20)
    away_numbers = Entry(player_entry_frame, width=5)
    away_players = Entry(player_entry_frame, width=20)
    
    home_numbers.grid(row=x+1, column=0, padx=5, pady=(0,3))
    home_players.grid(row=x+1, column=1, padx=(5,25))
    away_numbers.grid(row=x+1, column=2, padx=5, pady=(0,3))
    away_players.grid(row=x+1, column=3, padx=5)
    
    home_number_entries.append(home_numbers)
    home_player_entries.append(home_players)
    away_number_entries.append(away_numbers)
    away_player_entries.append(away_players)

submit_button = Button(base, text='Submit', command=submit_teams, font=button_font)
submit_button.pack()

error_label = Label(base, text='', font=reg_font, foreground="red")
error_label.pack()

base.mainloop()
