import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date
from joblib import load
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import ginput
from matplotlib.patches import Arc
from matplotlib.widgets import Cursor
from functools import partial
from Shot import Player, Shot
from mplsoccer.pitch import Pitch

model = load('xG_model/lgbm_model.joblib')

### Can't figure out how to add a cursor to the plot ###
# class BlittedCursor():
#     """
#     A cross hair cursor using blitting for faster redraw.
#     """
#     def __init__(self, ax):
#         self.ax = ax
#         self.background = None
#         self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
#         self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
#         # text location in axes coordinates
#         self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)
#         self._creating_background = False
#         ax.figure.canvas.mpl_connect('draw_event', self.on_draw)

#     def on_draw(self, event):
#         self.create_new_background()

#     def set_cross_hair_visible(self, visible):
#         need_redraw = self.horizontal_line.get_visible() != visible
#         self.horizontal_line.set_visible(visible)
#         self.vertical_line.set_visible(visible)
#         self.text.set_visible(visible)
#         return need_redraw

#     def create_new_background(self):
#         if self._creating_background:
#             # discard calls triggered from within this function
#             return
#         self._creating_background = True
#         self.set_cross_hair_visible(False)
#         self.ax.figure.canvas.draw()
#         plt.draw()
#         self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)
#         self.set_cross_hair_visible(True)
#         self._creating_background = False

#     def on_mouse_move(self, event):
#         if self.background is None:
#             self.create_new_background()
#         if not event.inaxes:
#             need_redraw = self.set_cross_hair_visible(False)
#             if need_redraw:
#                 self.ax.figure.canvas.restore_region(self.background)
#                 self.ax.figure.canvas.blit(self.ax.bbox)
#         else:
#             self.set_cross_hair_visible(True)
#             # update the line positions
#             x, y = event.xdata, event.ydata
#             self.horizontal_line.set_ydata(y)
#             self.vertical_line.set_xdata(x)
#             self.text.set_text('x=%1.2f, y=%1.2f' % (x, y))

#             self.ax.figure.canvas.restore_region(self.background)
#             self.ax.draw_artist(self.horizontal_line)
#             self.ax.draw_artist(self.vertical_line)
#             self.ax.draw_artist(self.text)
#             self.ax.figure.canvas.blit(self.ax.bbox)

def draw_pitch():
    global fig, ax
    pitch = Pitch(pitch_type='uefa', pitch_color='grass', goal_type='box', line_color='white', stripe=True)
    fig, ax = pitch.draw()

    #Hide axis
    plt.axis('off')

    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.ion()
    plt.show()
    
    
def onclick(event):
    global fig, ax, circle
    global home_goals, away_goals, home_shots, away_shots, home_SOT, away_SOT, shot_index
    
    x_loc = round(event.xdata,2)
    y_loc = round(event.ydata,2)
    
    if team_button1.pressed:
        team = "Home"
        team_name = home_team
        if(home_dropdown.get() == ''):
            shot_output.config(text='Please Choose a Player for the Shot', foreground="red")
            return
        split = home_dropdown.get().split("--")
        player_name = split[1]
        player_number = int(split[0])
    else:
        team = "Away"
        team_name = away_team
        if(away_dropdown.get() == ''):
            shot_output.config(text='Please Choose a Player for the Shot', foreground="red")
            return
        split = away_dropdown.get().split("--")
        player_name = split[1]
        player_number = int(split[0])
        
    if body_part_button1.pressed:
        body_part = 0
    else:
        body_part = 1
        
    if assist_type_button1.pressed:
        assist_type = 3
    elif assist_type_button2.pressed:
        assist_type = 0
    elif assist_type_button3.pressed:
        assist_type = 1
    elif assist_type_button4.pressed:
        assist_type = 2
    else: 
        assist_type = 4
        
    if shot_type_button1.pressed:
        shot_type = 4
    elif shot_type_button2.pressed:
        shot_type = 0
    elif shot_type_button3.pressed:
        shot_type = 1
    elif shot_type_button4.pressed:
        shot_type = 2
    else:
        shot_type = 3
        
    
    # Goal
    if str(event.key) == "shift" and str(event.button) == "MouseButton.LEFT":
        on_target = 1
        goal = 1
        new_shot = Shot(shot_index, team_name, player_name, player_number, on_target, goal, x_loc, y_loc, body_part, assist_type, shot_type)
        circle = plt.Circle((x_loc, y_loc), 1.0, color='red')
        ax.add_artist(circle)
        # +1 shots, SOT, and goal
        if team == "Home":
            home_goals += 1
            home_shots += 1
            home_SOT += 1
            score_home_label.configure(text=str(home_goals))
            shots_home_label.configure(text=str(home_shots))
            SOT_home_label.configure(text=str(home_SOT))
        else:
            away_goals += 1
            away_shots += 1
            away_SOT += 1
            score_away_label.configure(text=str(away_goals))
            shots_away_label.configure(text=str(away_shots))
            SOT_away_label.configure(text=str(away_SOT))
        shot_index += 1
    # Shot Off Target
    elif str(event.button) == "MouseButton.RIGHT":
        on_target = 0
        goal = 0
        new_shot = Shot(shot_index, team_name, player_name, player_number, on_target, goal, x_loc, y_loc, body_part, assist_type, shot_type)
        circle = plt.Circle((x_loc, y_loc), 1.0, color='blue')
        ax.add_artist(circle)
        # +1 shots
        if team == "Home":
            home_shots += 1
            shots_home_label.configure(text=str(home_shots))
        else:
            away_shots += 1
            shots_away_label.configure(text=str(away_shots))
        shot_index += 1
    # Shot On Target
    elif str(event.button) == "MouseButton.LEFT":
        on_target = 1
        goal = 0
        new_shot = Shot(shot_index, team_name, player_name, player_number, on_target, goal, x_loc, y_loc, body_part, assist_type, shot_type)
        circle = plt.Circle((x_loc, y_loc), 1.0, color='orange')
        ax.add_artist(circle)
        # +1 shots, SOT
        if team == "Home":
            home_shots+=1
            home_SOT += 1
            shots_home_label.configure(text=str(home_shots))
            SOT_home_label.configure(text=str(home_SOT))
        else:
            away_shots += 1
            away_SOT += 1
            shots_away_label.configure(text=str(away_shots))
            SOT_away_label.configure(text=str(away_SOT))
        shot_index += 1
        
    xG_output = calcXG(new_shot)
    display_location(x_loc, y_loc, new_shot, xG_output)
    createDict(new_shot, xG_output)
    plt.draw()
    

def calcXG(shot_obj):
    data = pd.DataFrame.from_dict([{'shot_type_name': shot_obj.getShotType(), 'x': shot_obj.getX(), 'y': shot_obj.getY(), 'body_part_name': shot_obj.getBodyPart(), 'assist_type': shot_obj.getAssistType()}])
    return round(model.predict_proba(data)[:,1][0], 5)
    

def display_location(x, y, shot, xG):
    string_x = str(round(x,1))
    string_y = str(round(y,1))
    shot_output.configure(text=f"xG: {xG}")

    
def createDict(shot_obj, xG):
    new_dict = dict({'shot_id': shot_obj.getIndex(), 'Team': shot_obj.getTeam(), 'player_name': shot_obj.getPlayerName(), 'player_number': shot_obj.getPlayerNumber(), 'onTarget': shot_obj.getOnTarget(), 'isGoal': shot_obj.getGoal(), 'x': shot_obj.getX(), 'y': shot_obj.getY(), 'body_part_name': shot_obj.getBodyPart(), 'assist_type': shot_obj.getAssistType(), 'shot_type_name': shot_obj.getShotType(), 'xG': xG})
    List.append(new_dict)
    

class TeamButton():
    def __init__(self, input_text, text_font, data_entry):
        self.input_text = input_text
        self.text_font = text_font
        self.data_entry = data_entry
        if self.input_text == "Home":
            self.pressed = True
            self.button = Button(self.data_entry, text=input_text, command=self.updateHome, relief=SUNKEN, font=self.text_font)
        else:
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updateAway, relief=RAISED, font=self.text_font)
    
    def updateHome(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            team_button2.button.configure(relief=RAISED)
            self.pressed = True
            team_button2.pressed = False
        
    def updateAway(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            team_button1.button.configure(relief=RAISED)
            self.pressed = True
            team_button1.pressed = False
            
            
class  BodyPartButton():
    def __init__(self, input_text, text_font, data_entry):
        self.input_text = input_text
        self.text_font = text_font
        self.data_entry = data_entry
        if self.input_text == "Foot":
            self.pressed = True
            self.button = Button(self.data_entry, text=input_text, command=self.updateFoot, relief=SUNKEN, font=self.text_font)
        else:
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updateOther, relief=RAISED, font=self.text_font)
    
    def updateFoot(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            body_part_button2.button.configure(relief=RAISED)
            self.pressed = True
            body_part_button2.pressed = False
        
    def updateOther(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            body_part_button1.button.configure(relief=RAISED)
            self.pressed = True
            body_part_button1.pressed = False
           
        
class AssistTypeButton():
    def __init__(self, input_text, text_font, data_entry):
        self.input_text = input_text
        self.text_font = text_font
        self.data_entry = data_entry
        if self.input_text == "Direct":
            self.pressed = True
            self.button = Button(self.data_entry, text=input_text, command=self.updateDirect, relief=SUNKEN, font=self.text_font)
        elif self.input_text == "Pass":
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updatePass, relief=RAISED, font=self.text_font)
        elif self.input_text == "Recovery":
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updateRecovery, relief=RAISED, font=self.text_font)
            
        elif self.input_text == "Clearance":
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updateClearance, relief=RAISED, font=self.text_font)
        else:  # Rebound Button
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updateRebound, relief=RAISED, font=self.text_font)
    
    def updateDirect(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            assist_type_button2.button.configure(relief=RAISED)
            assist_type_button3.button.configure(relief=RAISED)
            assist_type_button4.button.configure(relief=RAISED)
            assist_type_button5.button.configure(relief=RAISED)
            self.pressed = True
            assist_type_button2.pressed = False
            assist_type_button3.pressed = False
            assist_type_button4.pressed = False
            assist_type_button5.pressed = False
        
    def updatePass(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            assist_type_button1.button.configure(relief=RAISED)
            assist_type_button3.button.configure(relief=RAISED)
            assist_type_button4.button.configure(relief=RAISED)
            assist_type_button5.button.configure(relief=RAISED)
            self.pressed = True
            assist_type_button1.pressed = False
            assist_type_button3.pressed = False
            assist_type_button4.pressed = False
            assist_type_button5.pressed = False
    
    def updateRecovery(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            assist_type_button1.button.configure(relief=RAISED)
            assist_type_button2.button.configure(relief=RAISED)
            assist_type_button4.button.configure(relief=RAISED)
            assist_type_button5.button.configure(relief=RAISED)
            self.pressed = True
            assist_type_button1.pressed = False
            assist_type_button2.pressed = False
            assist_type_button4.pressed = False
            assist_type_button5.pressed = False
            
    def updateClearance(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            assist_type_button1.button.configure(relief=RAISED)
            assist_type_button2.button.configure(relief=RAISED)
            assist_type_button3.button.configure(relief=RAISED)
            assist_type_button5.button.configure(relief=RAISED)
            self.pressed = True
            assist_type_button1.pressed = False
            assist_type_button2.pressed = False
            assist_type_button3.pressed = False
            assist_type_button5.pressed = False
            
    def updateRebound(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            assist_type_button1.button.configure(relief=RAISED)
            assist_type_button2.button.configure(relief=RAISED)
            assist_type_button3.button.configure(relief=RAISED)
            assist_type_button4.button.configure(relief=RAISED)
            self.pressed = True
            assist_type_button1.pressed = False
            assist_type_button2.pressed = False
            assist_type_button3.pressed = False
            assist_type_button4.pressed = False
            
            
class ShotTypeButton():
    def __init__(self, input_text, text_font, data_entry):
        self.input_text = input_text
        self.text_font = text_font
        self.data_entry = data_entry
        if self.input_text == "Open Play":
            self.pressed = True
            self.button = Button(self.data_entry, text=input_text, command=self.updateOpenPlay, relief=SUNKEN, font=self.text_font)
        elif self.input_text == "Free Kick":
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updateFreeKick, relief=RAISED, font=self.text_font)
        elif self.input_text == "Corner":
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updateCorner, relief=RAISED, font=self.text_font)
        elif self.input_text == "Throw In":
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updateThrowIn, relief=RAISED, font=self.text_font)
        else: # Direct Set Piece
            self.pressed = False
            self.button = Button(self.data_entry, text=input_text, command=self.updateDirectSetPiece, relief=RAISED, font=self.text_font)
    
    def updateOpenPlay(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            shot_type_button2.button.configure(relief=RAISED)
            shot_type_button3.button.configure(relief=RAISED)
            shot_type_button4.button.configure(relief=RAISED)
            shot_type_button5.button.configure(relief=RAISED)
            self.pressed = True
            shot_type_button2.pressed = False
            shot_type_button3.pressed = False
            shot_type_button4.pressed = False
            shot_type_button5.pressed = False
            
    def updateFreeKick(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            shot_type_button1.button.configure(relief=RAISED)
            shot_type_button3.button.configure(relief=RAISED)
            shot_type_button4.button.configure(relief=RAISED)
            shot_type_button5.button.configure(relief=RAISED)
            self.pressed = True
            shot_type_button1.pressed = False
            shot_type_button3.pressed = False
            shot_type_button4.pressed = False
            shot_type_button5.pressed = False
        
    def updateCorner(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            shot_type_button1.button.configure(relief=RAISED)
            shot_type_button2.button.configure(relief=RAISED)
            shot_type_button4.button.configure(relief=RAISED)
            shot_type_button5.button.configure(relief=RAISED)
            self.pressed = True
            shot_type_button1.pressed = False
            shot_type_button2.pressed = False
            shot_type_button4.pressed = False
            shot_type_button5.pressed = False
            
    def updateThrowIn(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            shot_type_button1.button.configure(relief=RAISED)
            shot_type_button2.button.configure(relief=RAISED)
            shot_type_button3.button.configure(relief=RAISED)
            shot_type_button5.button.configure(relief=RAISED)
            self.pressed = True
            shot_type_button1.pressed = False
            shot_type_button2.pressed = False
            shot_type_button3.pressed = False
            shot_type_button5.pressed = False
            
    def updateDirectSetPiece(self):
        if self.pressed == False:
            self.button.configure(relief=SUNKEN)
            shot_type_button1.button.configure(relief=RAISED)
            shot_type_button2.button.configure(relief=RAISED)
            shot_type_button3.button.configure(relief=RAISED)
            shot_type_button4.button.configure(relief=RAISED)
            self.pressed = True
            shot_type_button1.pressed = False
            shot_type_button2.pressed = False
            shot_type_button3.pressed = False
            shot_type_button4.pressed = False
            
    
def saveCSV():
    # save all the data in placeholders to a csv/excel file
    today = date.today()
    today = today.strftime("%b-%d-%Y")
    df = pd.DataFrame(List)
    boolean_cat = {0: False, 1: True}
    shot_type_cat = {0: 'free kick', 1: 'corner', 2: 'throw in', 3: 'dir set piece', 4: 'open play'}
    body_type_cat = {0: 'Foot', 1: 'Other'}
    assist_type_cat = {0: 'pass', 1: 'recovery', 2: 'clearance', 3: 'direct', 4: 'rebound'}
    df.onTarget.replace(boolean_cat, inplace=True)
    df.isGoal.replace(boolean_cat, inplace=True)
    df.shot_type_name.replace(shot_type_cat, inplace=True)
    df.body_part_name.replace(body_type_cat, inplace=True)
    df.assist_type.replace(assist_type_cat, inplace=True)
    home_team_underscore = home_team.replace(" ", "_")
    away_team_underscore = away_team.replace(" ", "_")
    df.to_csv(f'output/{home_team_underscore}_vs_{away_team_underscore}{today}.csv')
    
    
def removeLast():
    global home_goals, away_goals, home_shots, away_shots, home_SOT, away_SOT, shot_index
    if len(List) != 0:
        circle.remove()
        removed_shot = List.pop()
        
        if removed_shot['Team'] == home_team:
            if removed_shot['isGoal'] == 1:
                home_goals -= 1
                score_home_label.configure(text=str(home_goals))
            if removed_shot['onTarget'] == 1:
                home_SOT -= 1
                SOT_home_label.configure(text=str(home_SOT))
            home_shots -= 1
            shots_home_label.configure(text=str(home_shots))
        else:
            if removed_shot['isGoal'] == 1:
                away_goals -= 1
                score_away_label.configure(text=str(away_goals))
            if removed_shot['onTarget'] == 1:
                away_SOT -= 1
                SOT_away_label.configure(text=str(away_SOT))
            away_shots -= 1
            shots_away_label.configure(text=str(away_shots))
        shot_index -= 1
        
        
        
home_number_entries = []
home_player_entries = []
away_number_entries = []
away_player_entries = []

global home_team, away_team, home_list, away_list

def submit_teams():
    global home_team, away_team, home_list, away_list
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
    
    base.destroy()
    

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


root = Tk()
# root.geometry("584x643")
# root.resizable(width=False, height=False)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)


global fig, ax, circle
global home_goals, away_goals, home_shots, away_shots, home_SOT, away_SOT, shot_index

home_goals = 0
away_goals = 0
home_shots = 0
away_shots = 0
home_SOT = 0
away_SOT = 0
shot_index = 0
List = []

team_label_font = tkFont.Font(family='Helvetica', size=20, weight='bold')
team_entry_font = tkFont.Font(family='Hevetica', size=15)
button_font = tkFont.Font(family='Hevetica', size=12)
reg_font = tkFont.Font(family='Hevetica', size=12)


team_frame = LabelFrame(root, padx=10, pady=10)
team_frame.pack(side=TOP, padx=10, pady=10)

home_label = Label(team_frame, text="Home", font=team_label_font)
away_label = Label(team_frame, text="Away", font=team_label_font)

home_label.grid(row=0, column=0, sticky=N+S+E+W)
away_label.grid(row=0, column=3, sticky=N+S+E+W)

home_name_label = Label(team_frame, text=home_team, font=team_entry_font)
away_name_label = Label(team_frame, text=away_team, font=team_entry_font)
home_name_label.grid(row=1, column=0, padx=(0,20)) # sticky=N+S+E+W)
away_name_label.grid(row=1, column=3, padx=(20,0)) #, sticky=N+S+E+W)

button_frame = LabelFrame(root)
button_frame.pack(padx=10, pady=10)
button1 = Button(button_frame, text='Show Pitch', command=draw_pitch, font=button_font)
button1.pack(padx=(5, 50), pady=5, side=LEFT)

save_file_button = Button(button_frame, text='Save Data as .CSV', command=saveCSV, font=button_font)
save_file_button.pack(padx=(50,5), pady=5, side=RIGHT)

outer = LabelFrame(root)
outer.pack(padx=10, pady=10)

key = LabelFrame(outer, text="Key", font=reg_font)
key.pack(side=LEFT)
key_text1 = Label(key, text="Shot On Target: LClick (Orange)", font=reg_font)
key_text2 = Label(key, text="Shot Off Target: RClick (Blue)", font=reg_font)
key_text3 = Label(key, text="Goal: 'shift' + LClick (Red)", font=reg_font)
key_text1.pack(fill=BOTH, expand=YES)
key_text2.pack(fill=BOTH, expand=YES)
key_text3.pack(fill=BOTH, expand=YES)

scoreboard = LabelFrame(outer, text="Game Scoreboard", font=reg_font)
scoreboard.pack(side=RIGHT)
scoreboard_home = Label(scoreboard, text="Home", font=reg_font)
scoreboard_away = Label(scoreboard, text="Away", font=reg_font)
shots_label = Label(scoreboard, text="Shots: ", font=reg_font)
score_frame1 = LabelFrame(scoreboard)
score_frame2 = LabelFrame(scoreboard)
score_home_label = Label(score_frame1, text=str(home_goals), font=reg_font)
score_away_label = Label(score_frame2, text=str(away_goals), font=reg_font)
shots_home_label = Label(scoreboard, text=str(home_shots), font=reg_font)
shots_away_label = Label(scoreboard, text=str(away_shots), font=reg_font)
SOT_label = Label(scoreboard, text="SOT: ", font=reg_font)
SOT_home_label = Label(scoreboard, text=str(home_SOT), font=reg_font)
SOT_away_label = Label(scoreboard, text=str(away_SOT), font=reg_font)
scoreboard_home.grid(row=0, column=1)
scoreboard_away.grid(row=0, column=2)
score_frame1.grid(row=1, column=1)
score_frame2.grid(row=1, column=2)
score_home_label.pack()
score_away_label.pack()
shots_label.grid(row=2, column=0)
shots_home_label.grid(row=2, column=1)
shots_away_label.grid(row=2, column=2)
SOT_label.grid(row=3, column=0)
SOT_home_label.grid(row=3, column=1)
SOT_away_label.grid(row=3, column=2)

# xG Input Section
data_entry = LabelFrame(root, text="xG Input", padx=10, font=reg_font)
data_entry.pack(padx=10, pady=10)

team = Label(data_entry, text="Team: ", font=reg_font)
team_button1 = TeamButton("Home", button_font, data_entry)
team_button2 = TeamButton("Away", button_font, data_entry)
body_part = Label(data_entry, text="Body Part: ", font=reg_font)
body_part_button1 = BodyPartButton("Foot", button_font, data_entry)
body_part_button2 = BodyPartButton("Other", button_font, data_entry)
assist_type = Label(data_entry, text="Assist Type: ", font=reg_font)
assist_type_button1 = AssistTypeButton("Direct", button_font, data_entry)
assist_type_button2 = AssistTypeButton("Pass", button_font, data_entry)
assist_type_button3 = AssistTypeButton("Recovery", button_font, data_entry)
assist_type_button4 = AssistTypeButton("Clearance", button_font, data_entry)
assist_type_button5 = AssistTypeButton("Rebound", button_font, data_entry)
shot_type = Label(data_entry, text="Shot Type: ", font=reg_font)
shot_type_button1 = ShotTypeButton("Open Play", button_font, data_entry)
shot_type_button2 = ShotTypeButton("Free Kick", button_font, data_entry)
shot_type_button3 = ShotTypeButton("Corner", button_font, data_entry)
shot_type_button4 = ShotTypeButton("Throw In", button_font, data_entry)
shot_type_button5 = ShotTypeButton("Direct Set Piece", button_font, data_entry)
home_dropdown_label = Label(data_entry, text="Home Player: ", font=reg_font)
away_dropdown_label = Label(data_entry, text="Away Player: ", font=reg_font)
home_dropdown_values = list(str(player.getNumber()) + "--" + player.getName() for player in home_list)
away_dropdown_values = list(str(player.getNumber()) + "--" + player.getName() for player in away_list)
home_dropdown = ttk.Combobox(data_entry, width=20, values=home_dropdown_values)
away_dropdown = ttk.Combobox(data_entry, width=20, values=away_dropdown_values)
shot_output = Label(data_entry, text="Output", font=reg_font)
remove_last_button = Button(root, text='Remove Last Entry', command=removeLast, font=button_font)

team.grid(row=0, column=0)
team_button1.button.grid(row=0, column=1, padx=5, pady=5)
team_button2.button.grid(row=0, column=2, padx=5, pady=5)
body_part.grid(row=1, column=0)
body_part_button1.button.grid(row=1, column=1, padx=5, pady=5)
body_part_button2.button.grid(row=1, column=2, padx=5, pady=5)
assist_type.grid(row=2, column=0)
assist_type_button1.button.grid(row=2, column=1, padx=5, pady=5)
assist_type_button2.button.grid(row=2, column=2, padx=5, pady=5)
assist_type_button3.button.grid(row=2, column=3, padx=5, pady=5)
assist_type_button4.button.grid(row=2, column=4, padx=5, pady=5)
assist_type_button5.button.grid(row=2, column=5, padx=5, pady=5)
shot_type.grid(row=3, column=0)
shot_type_button1.button.grid(row=3, column=1, padx=5, pady=5)
shot_type_button2.button.grid(row=3, column=2, padx=5, pady=5)
shot_type_button3.button.grid(row=3, column=3, padx=5, pady=5)
shot_type_button4.button.grid(row=3, column=4, padx=5, pady=5)
shot_type_button5.button.grid(row=3, column=5, padx=5, pady=5)
home_dropdown_label.grid(row=5, column=1, padx=5, pady=5)
home_dropdown.grid(row=5, column=2, padx=(5,10), pady=5)
away_dropdown_label.grid(row=5, column=3, padx=(10,5), pady=5)
away_dropdown.grid(row=5, column=4, padx=5, pady=5)
home_dropdown.current()
away_dropdown.current()
shot_output.grid(row=6, column=2)
remove_last_button.pack()

root.mainloop()
    
    
