#!/usr/bin/env python
# coding: utf-8


# Import necessary libraries
import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')


# Read in data
df_arrests = pd.read_csv('Arrests by Race 2016.csv', thousands=',')
df_deaths = pd.read_csv('Fatal Shootings.csv')


# Clean up formatting for arrest data and drop 'id' column for death data
df_arrests.columns = df_arrests.iloc[1]
df_arrests = df_arrests.drop([0, 1])
df_deaths = df_deaths.drop(['id'], axis=1)


# Build new dataframe for the number of deaths (armed and unarmed) by race
df_deaths['date'] = df_deaths['date'].apply(pd.to_datetime, errors='coerce')
deaths_2016 = df_deaths[df_deaths['date'] >= '2016-01-01'][df_deaths['date'] < '2017-01-01']

armed = pd.DataFrame(deaths_2016[deaths_2016['armed'] != 'unarmed']['race'].value_counts(dropna=False))
armed = armed.reset_index()
armed = armed.rename(columns={'index': 'Race', 'race': 'Number of Deaths'})
armed['Armed'] = 'Yes'

unarmed = pd.DataFrame(deaths_2016[deaths_2016['armed'] == 'unarmed']['race'].value_counts(dropna=False))
unarmed = unarmed.reset_index()
unarmed = unarmed.rename(columns={'index': 'Race', 'race': 'Number of Deaths'})
unarmed['Armed'] = 'No'

df_race = armed.append(unarmed, ignore_index=True)
race_names = {'W': 'White', 'B': 'Black', 'H': 'Hispanic', 'N': 'Native', 'A': 'Asian', 'O': 'Other'}
df_race['Race'] = df_race['Race'].replace(race_names)
df_race['Race'] = np.where(df_race['Race'].isna(), 'Unknown', df_race['Race'])

total_deaths = int(df_race.sum(numeric_only=True, skipna=True))
df_race['Percent Deaths'] = (df_race['Number of Deaths']/total_deaths)*100


# Build a new series of the number of arrests by race, join to race data
# Note: Data on hispanic arrests isn't gathered by all agencies, hence percentages will not total 100
arrests_row = df_arrests.loc[[2]]
column_names = ['Number', 'Percent']

white = arrests_row['White']
white.columns = column_names
black = arrests_row['Black or\nAfrican\nAmerican']
black.columns = column_names
asian = arrests_row['Asian']
asian.columns = column_names
native = arrests_row['American\nIndian or\nAlaska\nNative']
native.columns = column_names
hispan = arrests_row['Hispanic\nor\nLatino']
hispan.columns = column_names

arrests = pd.DataFrame({'Race': ['White', 'Black', 'Asian', 'Native', 'Hispanic']})
arrests['Number of Arrests'] = ''
arrests['Number of Arrests'] = np.where(arrests['Race'] == 'White', white['Number'], arrests['Number of Arrests'])
arrests['Number of Arrests'] = np.where(arrests['Race'] == 'Black', black['Number'], arrests['Number of Arrests'])
arrests['Number of Arrests'] = np.where(arrests['Race'] == 'Asian', asian['Number'], arrests['Number of Arrests'])
arrests['Number of Arrests'] = np.where(arrests['Race'] == 'Native', native['Number'], arrests['Number of Arrests'])
arrests['Number of Arrests'] = np.where(arrests['Race'] == 'Hispanic', hispan['Number'], arrests['Number of Arrests'])

arrests['Percent Arrests'] = ''
arrests['Percent Arrests'] = np.where(arrests['Race'] == 'White', white['Percent'], arrests['Percent Arrests'])
arrests['Percent Arrests'] = np.where(arrests['Race'] == 'Black', black['Percent'], arrests['Percent Arrests'])
arrests['Percent Arrests'] = np.where(arrests['Race'] == 'Asian', asian['Percent'], arrests['Percent Arrests'])
arrests['Percent Arrests'] = np.where(arrests['Race'] == 'Native', native['Percent'], arrests['Percent Arrests'])
arrests['Percent Arrests'] = np.where(arrests['Race'] == 'Hispanic', hispan['Percent'], arrests['Percent Arrests'])

arrests['Number of Arrests'] = arrests['Number of Arrests'].astype(str).str.replace(',', '')
df_race = df_race.merge(arrests, on='Race', how='left')


# Create new row for totals
df_race['Number of Deaths'] = df_race['Number of Deaths'].apply(pd.to_numeric, errors='coerce')
df_race['Percent Deaths'] = df_race['Percent Deaths'].apply(pd.to_numeric, errors='coerce')
df_race['Number of Arrests'] = df_race['Number of Arrests'].apply(pd.to_numeric, errors='coerce')
df_race['Percent Arrests'] = df_race['Percent Arrests'].apply(pd.to_numeric, errors='coerce')

df_race = df_race.append(df_race[df_race['Armed'] == 'Yes'].sum(numeric_only=True), ignore_index=True)
df_race['Race'] = np.where(df_race.isna(), 'Total', df_race)
df_race.at[11,'Armed'] = 'Yes'
df_race = df_race.append(df_race[df_race['Armed'] == 'No'].sum(numeric_only=True), ignore_index=True)
df_race['Race'] = np.where(df_race.isna(), 'Total', df_race)
df_race.at[12,'Armed'] = 'No'


# Build a new column in race data for number killed per arrest
df_race['Deaths per Arrest'] = df_race['Number of Deaths']/df_race['Number of Arrests']
df_race['Deaths per 1,000,000 Arrests'] = df_race['Number of Deaths']/df_race['Number of Arrests']*1000000


# Visualize number killed by race per arrest, armed vs. unarmed
plt.figure(figsize=(10, 5))
bars = ['Total', 'White', 'Black', 'Hispanic', 'Asian', 'Native']
color = ['#570003', '#b80006']

plot = sns.barplot(x='Race', y='Deaths per 1,000,000 Arrests', data=df_race, order=bars, palette=color, hue='Armed')
plt.ylim(0,150)
plt.setp(plot.patches, linewidth=0)

font = {'fontname':'Helvetica'}
plt.title('Fatal Police Shootings in the U.S. per 1,000,000 Arrests, 2016',**font)
plt.xlabel('Race',**font)
plt.ylabel('Deaths per 1,000,000 Arrests',**font)
plt.xticks(**font)
plt.savefig('Shootings per Arrest (Armed vs. Unarmed).png')


# Visualize number killed by race per arrest, unarmed
plt.figure(figsize=(10, 5))
bars = ['Total', 'White', 'Black', 'Hispanic', 'Asian', 'Native']
color = ['#b80006']

plot = sns.barplot(x='Race', y='Deaths per 1,000,000 Arrests', data=df_race, order=bars, palette=color, hue='Armed',
                   hue_order=['No'])
plt.ylim(0,10)
plt.setp(plot.patches, linewidth=0)

font = {'fontname':'Helvetica'}
plt.title('Unarmed Fatal Police Shootings in the U.S. per 1,000,000 Arrests, 2016',**font)
plt.xlabel('Race',**font)
plt.ylabel('Deaths per 1,000,000 Arrests',**font)
plt.xticks(**font)
plot.legend_.remove()
plt.savefig('Unarmed Shootings per Arrest.png')