#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import necessary programs
import os
import sys

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

import json
import csv

import os,glob

import statsmodels.api as sm


# The data that is used in this model is from the free data source provided by StatsBomb
# <img src = "stats-bomb-logo.png"/>

# In[2]:


#Read through all json files in folder and combine them
myList = []
folder_path = r'C:\Users\Yuma\Desktop\Sport Analytics\StatsBomb Data\open-data-master\data\events'
for filename in glob.glob(os.path.join(folder_path,'*.json')):
    with open(filename,'r',encoding='utf-8') as f:
        myList += json.load(f)
print(len(myList))


# In[3]:


#Only get shot data from json
shot_data = []
length = len(myList)
for i in range(length):
    if myList[i]["type"]["name"] == "Shot":
        shot_data.append(myList[i])

print(len(shot_data))


# In[4]:


print(shot_data[162])


# In[5]:


#Display elements of shot data
for i in range(len(shot_data)):
    print(shot_data[i]['shot']['statsbomb_xg'])


# In[6]:


new_shot_data = []
for i in range(len(shot_data)):
    #Get rid of PK shots because we already know PKs have a 0.76 xG
    if 'statsbomb_xg' in shot_data[i]['shot']:
        if not (shot_data[i]['shot'].get('statsbomb_xg') == 0.76):
            Dict = dict({'id': shot_data[i]['id'], 'play_pattern': shot_data[i]['play_pattern']['name'], 'location': 
                     shot_data[i]['location'], 'statsbomb_xg': shot_data[i]['shot']['statsbomb_xg'], 'end_location': 
                     shot_data[i]['shot']['end_location'], 'body_part': shot_data[i]['shot']['body_part']['name'], 
                     'technique': shot_data[i]['shot']['technique']['name'], 'outcome': 
                     shot_data[i]['shot']['outcome']['name'], 'under_pressure': False, 'first_time': False})
            if 'under_pressure' in shot_data[i].keys():
                Dict.update(under_pressure = shot_data[i]['under_pressure'])
            if 'first_time' in shot_data[i]['shot'].keys():
                Dict.update(first_time = shot_data[i]['shot']['first_time'])
            new_shot_data.append(Dict)
    
print(len(new_shot_data))


# In[7]:


print(new_shot_data[174])


# In[8]:


for i in range(len(new_shot_data)):
    print(new_shot_data[i]['location'])
#print(new_shot_data[130]['location'])


# In[9]:


print(new_shot_data[0]['location'])


# In[10]:


#Calculate 'distance' data from 'location' data
distance = []
goal = [120,40]
for i in range(len(new_shot_data)):
    point = new_shot_data[i]['location']
    calculation = math.sqrt(((point[0]-goal[0])**2) + ((point[1]-goal[1])**2))
    distance.append(calculation)

print(distance[10000])


# In[11]:


#Calculate 'angle' data from 'location' data
angle = []
pen_vect_pt = [12,0]
for i in range(len(new_shot_data)):
    shot_vector = [120-new_shot_data[i]['location'][0],abs(40-new_shot_data[i]['location'][1])]
    unit_vector_1 = pen_vect_pt / np.linalg.norm(pen_vect_pt)
    unit_vector_2 = shot_vector / np.linalg.norm(shot_vector)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    current_angle = math.degrees(np.arccos(dot_product))
    angle.append(current_angle)

print(angle)


# In[12]:


#Create a different json for the linear regression model
# 0 means false, 1 meeans true
new_shot_data_2 = []
for i in range(len(new_shot_data)):
    Dict_2 = dict({'id': new_shot_data[i]['id'] , 'location': new_shot_data[i]['location'], 'distance': distance[i], 
                   'angle': angle[i], 'isFoot': 0, 'isHead': 0, 'isVolley': 0, 'isNormalShot': 0, 'isLobShot': 0, 
                   'isCorner': 0, 'isRegularPlay': 0, 'isFreeKick': 0, 'isThrowIn': 0, 'isCounter': 0, 'fromKeeper': 0, 
                   'fromGK': 0, 'first_time': 0, 'under_pressure': 0, 'isGoal': 0, 
                   'statsbomb_xg': new_shot_data[i]['statsbomb_xg']})
    
    if new_shot_data[i]['body_part'] == 'Right Foot':
        Dict_2.update(isFoot = 1)
    elif new_shot_data[i]['body_part'] == 'Left Foot':
        Dict_2.update(isFoot = 1)
    else:
        Dict_2.update(isFoot = 0)
        
    if new_shot_data[i]['body_part'] == 'Head':
        Dict_2.update(isHead = 1)
    else:
        Dict_2.update(isHead = 0)
        
    if new_shot_data[i]['technique'] == 'Half Volley':
        Dict_2.update(isVolley = 1)
    elif new_shot_data[i]['technique'] == 'Volley':
        Dict_2.update(isVolley = 1)
    else:
        Dict_2.update(isVolley = 0)
        
    if new_shot_data[i]['technique'] == 'Normal':
        Dict_2.update(isNormalShot = 1)
    else:
        Dict_2.update(isNormalShot = 0)
        
    if new_shot_data[i]['technique'] == 'Lob':
        Dict_2.update(isLobShot = 1)
    else:
        Dict_2.update(isLobShot = 0)
        
    if new_shot_data[i]['play_pattern'] == 'From Corner':
        Dict_2.update(isCorner = 1)
    else:
        Dict_2.update(isCorner = 0)
        
    if new_shot_data[i]['play_pattern'] == 'Regular Play':
        Dict_2.update(isRegularPlay = 1)
        
    if new_shot_data[i]['play_pattern'] == 'From Free Kick':
        Dict_2.update(isFreeKick = 1)
    else:
        Dict_2.update(isFreeKick = 0)
        
    if new_shot_data[i]['play_pattern'] == 'From Throw In':
        Dict_2.update(isThrowIn = 1)
    else:
        Dict_2.update(isThrowIn = 0)
        
    if new_shot_data[i]['play_pattern'] == 'From Counter':
        Dict_2.update(isCounter = 1)
    else:
        Dict_2.update(isCounter = 0)
        
    if new_shot_data[i]['play_pattern'] == 'From Keeper':
        Dict_2.update(fromKeeper = 1)
    else:
        Dict_2.update(fromKeeper = 0)
    
    if new_shot_data[i]['play_pattern'] == 'From Goal Kick':
        Dict_2.update(fromGK = 1)
    else:
        Dict_2.update(fromGK = 0)
        
    if new_shot_data[i]['under_pressure'] == True:
        Dict_2.update(under_pressure = 1)
    else:
        Dict_2.update(under_pressure = 0)
        
    if new_shot_data[i]['first_time'] == True:
        Dict_2.update(first_time = 1)
    else:
        Dict_2.update(first_time = 0)
        
    if new_shot_data[i]['outcome'] == 'Goal':
        Dict_2.update(isGoal = 1)
    else:
        Dict_2.update(isGoal = 0)
        
    new_shot_data_2.append(Dict_2)
    

print(new_shot_data_2[10000])


# In[13]:


#Save data as a csv file so we don't have to parse through original data over and over again
headers = ['id', 'location', 'distance', 'angle', 'isFoot', 'isHead', 'isVolley', 'isNormalShot', 'isLobShot', 'isCorner', 
           'isRegularPlay', 'isFreeKick', 'isThrowIn', 'isCounter', 'fromKeeper', 'fromGK', 'first_time', 'under_pressure', 
          'isGoal', 'statsbomb_xg']

filename = "shot_data.csv"

with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = headers)
    writer.writeheader()
    writer.writerows(new_shot_data_2)


# In[14]:


#Read json through pandas dataframe
df = pd.DataFrame(new_shot_data_2, columns=['id','location','distance', 'angle','isFoot','isHead','isVolley','isNormalShot', 
                                            'isLobShot', 'isCorner','isRegularPlay','isFreeKick','isThrowIn','isCounter',
                                            'fromKeeper', 'fromGK','first_time','under_pressure','isGoal','statsbomb_xg'])
print(df)


# In[15]:


#Eliminate duplicate data
df.drop_duplicates(subset = 'id', keep = False, inplace = True)
print(len(df))


# In[16]:


print(df[['isFoot', 'isVolley']])


# In[17]:


#Logistic Regression Calculation
#Got rid of 'isNormalShot', 'isCounter', 'fromKeeper', 'fromGK' because the p-value was too high
x = df[['distance', 'angle', 'isHead', 'isVolley', 'isLobShot', 'isNormalShot', 'isFreeKick', 'isCorner', 
        'under_pressure', 'first_time']]
y = df['isGoal']

model = sm.Logit(y,x).fit()
predictions = model.predict(x)
print(model.summary2())


# The next two sets of code are taken from Peter McKeever's Expected Goals Model program. It can be found here: http://petermckeever.com/2019/01/building-an-expected-goals-model-in-python/

# In[18]:


#Split and randomise our data into training and testing sets and see how accurate the model is on the test data
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

log_r = LogisticRegression()

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.3, random_state = 52)

log_r.fit(x_train, y_train)
print("Log Regression test set accuracy {:.3f}".format(log_r.score(x_test,y_test)))


# In[19]:


prediction = log_r.predict(x_test)

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, prediction)
print(confusion_matrix)


# The below program comes from Susan Li's article on "Building A Logistic Regression in Python, Step by Step" and can be found here: https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8

# In[20]:


#Draw a ROC curve to better understand our logistic regression model
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

logit_roc_auc = roc_auc_score(y_test, log_r.predict(x_test))
fpr, tpr, thresholds = roc_curve(y_test, log_r.predict_proba(x_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()


# In[21]:


#Output of xG values
xg_model = log_r.predict_proba(x)
for i in range(len(xg_model)):
    print(xg_model[i][1])


# Below is where you can apply the expected goals model to new datasets.

# In[22]:


#Import dataset and calculate distance and angle
test_df = pd.read_csv(r'C:\Users\Yuma\Desktop\Sport Analytics\xG_Model_Data.csv')
distance = []
goal = [120,40]
for i in range(len(test_df)):
    point_x = test_df.loc[i]['x_location']
    point_y = test_df.loc[i]['y_location']
    calculation = math.sqrt((point_x-goal[0])**2) + ((point_y-goal[1])**2)
    distance.append(calculation)
    
angle = []
pen_vect_pt = [12,0]
for i in range(len(test_df)):
    shot_vector = [120-test_df.loc[i]['x_location'],abs(40-test_df.loc[i]['y_location'])]
    unit_vector_1 = pen_vect_pt / np.linalg.norm(pen_vect_pt)
    unit_vector_2 = shot_vector / np.linalg.norm(shot_vector)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    current_angle = math.degrees(np.arccos(dot_product))
    angle.append(current_angle)

test_df['distance'] = distance
test_df['angle'] = angle
print(test_df)


# In[23]:


test_x = test_df[['distance', 'angle', 'isHead', 'isVolley', 'isLobShot', 'isNormalShot', 'isFreeKick', 'isCorner', 
        'under_pressure', 'first_time']]
test_xG = log_r.predict_proba(test_x)
print("The probability that the shot is a goal is: ")
print(test_xG[0][1])

