import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from joblib import load
import os
import argparse
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import ginput
from matplotlib.patches import Arc
from matplotlib.widgets import Cursor
from functools import partial
from mplsoccer.pitch import Pitch
from matplotlib.lines import Line2D

def Read_Data(file):
    global df_team1, df_team2, team1, team2, team1_xG_total, team2_xG_total
    df = pd.read_csv(file)

    mask = df["Team"] == df["Team"][0]
    df_team1 = df[mask].reset_index(drop=True)
    df_team2 = df[~mask].reset_index(drop=True)
    
    team1 = df_team1["Team"][0]
    team2 = df_team2["Team"][0]

    team1_xG_total = round(df_team1['xG'].sum(), 3)
    team2_xG_total = round(df_team2['xG'].sum(), 3)
    print("xG Totals")
    print(team1, team1_xG_total)
    print(team2, team2_xG_total)

def draw_pitch2(team):
    global fig, ax
    pitch = Pitch(pitch_type='uefa', pitch_color='grass', goal_type='box', line_color='white', stripe=True)
    fig, ax = pitch.draw()

    #Hide axis
    plt.axis('off')
    plt.suptitle(team, fontsize=25)
    if team == team1:
        plt.title('xG Total: ' + str(team1_xG_total), fontsize=18)
    else:
        plt.title('xG Total: ' + str(team2_xG_total), fontsize=18)
        
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Goal',
                          markerfacecolor='red', markersize=12), Line2D([0], [0], marker='o', color='w', label='Shot On Target',
                          markerfacecolor='orange', markersize=12), Line2D([0], [0], marker='o', color='w', label='Shot Off Target',
                          markerfacecolor='yellow', markersize=12)]
    ax.legend(handles=legend_elements, loc='upper left')
    
    
def mapShots(df, team):
    draw_pitch2(team)
    for index, shots in df.iterrows():
        if shots['isGoal'] == True:
            shot_color = 'red'
        elif shots['onTarget'] == True:
            shot_color = 'orange'
        else:
            shot_color = 'yellow'
        circle = plt.Circle((int(shots['x']), int(shots['y'])), 1.0, color=shot_color)
        ax.add_artist(circle)
        plt.draw()
    
    plt.show()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, type=str, help='csv file name')
    file_name = vars(parser.parse_args())['file']
    
    Read_Data(file_name)
    
    mapShots(df_team1, team1)
    mapShots(df_team2, team2)