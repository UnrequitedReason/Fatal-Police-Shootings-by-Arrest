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
arrests_2015 = pd.read_csv('Arrests by Race 2015.csv', thousands=',')
arrests_2016 = pd.read_csv('Arrests by Race 2016.csv', thousands=',')
arrests_2017 = pd.read_csv('Arrests by Race 2017.csv', thousands=',')
df_deaths = pd.read_csv('Fatal Shootings.csv')


# Clean up formatting for arrest data and drop 'id' column for death data
arrests_2015.columns = arrests_2015.iloc[1]
arrests_2015 = arrests_2015.drop([0, 1])
arrests_2016.columns = arrests_2016.iloc[1]
arrests_2016 = arrests_2016.drop([0, 1])
arrests_2017.columns = arrests_2017.iloc[1]
arrests_2017 = arrests_2017.drop([0, 1])
df_deaths = df_deaths.drop(['id'], axis=1)


# Build new dataframe for the number of deaths (armed and unarmed) by race
df_deaths['date'] = df_deaths['date'].apply(pd.to_datetime, errors='coerce')
deaths_2015 = df_deaths[df_deaths['date'] >= '2015-01-01'][df_deaths['date'] < '2016-01-01']
deaths_2016 = df_deaths[df_deaths['date'] >= '2016-01-01'][df_deaths['date'] < '2017-01-01']
deaths_2017 = df_deaths[df_deaths['date'] >= '2017-01-01'][df_deaths['date'] < '2018-01-01']

unarmed_2015 = pd.DataFrame(deaths_2015[deaths_2015['armed'] == 'unarmed']['race'].value_counts(dropna=False))
unarmed_2015 = unarmed_2015.reset_index()
unarmed_2015 = unarmed_2015.rename(columns={'index': 'Race', 'race': 'Number of Deaths'})
unarmed_2015['Armed'] = 'No'
unarmed_2015['Year'] = '2015'

unarmed_2016 = pd.DataFrame(deaths_2016[deaths_2016['armed'] == 'unarmed']['race'].value_counts(dropna=False))
unarmed_2016 = unarmed_2016.reset_index()
unarmed_2016 = unarmed_2016.rename(columns={'index': 'Race', 'race': 'Number of Deaths'})
unarmed_2016['Armed'] = 'No'
unarmed_2016['Year'] = '2016'

unarmed_2017 = pd.DataFrame(deaths_2017[deaths_2017['armed'] == 'unarmed']['race'].value_counts(dropna=False))
unarmed_2017 = unarmed_2017.reset_index()
unarmed_2017 = unarmed_2017.rename(columns={'index': 'Race', 'race': 'Number of Deaths'})
unarmed_2017['Armed'] = 'No'
unarmed_2017['Year'] = '2017'

df_race = unarmed_2015.append([unarmed_2016, unarmed_2017], ignore_index=True)
race_names = {'W': 'White', 'B': 'Black', 'H': 'Hispanic', 'N': 'Native', 'A': 'Asian', 'O': 'Other'}
df_race['Race'] = df_race['Race'].replace(race_names)
df_race['Race'] = np.where(df_race['Race'].isna(), 'Unknown', df_race['Race'])


# Build a new series of the number of arrests by race for 2015
# Note: Data on hispanic arrests isn't gathered by all agencies, hence percentages will not total 100
arrests_2015 = arrests_2015.loc[[2]]
column_names = ['Number', 'Percent']

white = arrests_2015['White']
white.columns = column_names
black = arrests_2015['Black or\nAfrican\nAmerican']
black.columns = column_names
asian = arrests_2015['Asian']
asian.columns = column_names
native = arrests_2015['American\nIndian or\nAlaska\nNative']
native.columns = column_names
hispan = arrests_2015['Hispanic\nor\nLatino']
hispan.columns = column_names

arrests_2015 = pd.DataFrame({'Race': ['White', 'Black', 'Asian', 'Native', 'Hispanic']})
arrests_2015['Number of Arrests'] = ''
arrests_2015['Number of Arrests'] = np.where(arrests_2015['Race'] == 'White', white['Number'],
                                             arrests_2015['Number of Arrests'])
arrests_2015['Number of Arrests'] = np.where(arrests_2015['Race'] == 'Black', black['Number'],
                                             arrests_2015['Number of Arrests'])
arrests_2015['Number of Arrests'] = np.where(arrests_2015['Race'] == 'Asian', asian['Number'],
                                             arrests_2015['Number of Arrests'])
arrests_2015['Number of Arrests'] = np.where(arrests_2015['Race'] == 'Native', native['Number'],
                                             arrests_2015['Number of Arrests'])
arrests_2015['Number of Arrests'] = np.where(arrests_2015['Race'] == 'Hispanic', hispan['Number'],
                                             arrests_2015['Number of Arrests'])

arrests_2015['Percent Arrests'] = ''
arrests_2015['Percent Arrests'] = np.where(arrests_2015['Race'] == 'White', white['Percent'],
                                           arrests_2015['Percent Arrests'])
arrests_2015['Percent Arrests'] = np.where(arrests_2015['Race'] == 'Black', black['Percent'],
                                           arrests_2015['Percent Arrests'])
arrests_2015['Percent Arrests'] = np.where(arrests_2015['Race'] == 'Asian', asian['Percent'],
                                           arrests_2015['Percent Arrests'])
arrests_2015['Percent Arrests'] = np.where(arrests_2015['Race'] == 'Native', native['Percent'],
                                           arrests_2015['Percent Arrests'])
arrests_2015['Percent Arrests'] = np.where(arrests_2015['Race'] == 'Hispanic', hispan['Percent'],
                                           arrests_2015['Percent Arrests'])

arrests_2015['Number of Arrests'] = arrests_2015['Number of Arrests'].astype(str).str.replace(',', '')
arrests_2015['Year'] = '2015'


# Build a new series of the number of arrests by race for 2016
# Note: Data on hispanic arrests isn't gathered by all agencies, hence percentages will not total 100
arrests_2016 = arrests_2016.loc[[2]]
column_names = ['Number', 'Percent']

white = arrests_2016['White']
white.columns = column_names
black = arrests_2016['Black or\nAfrican\nAmerican']
black.columns = column_names
asian = arrests_2016['Asian']
asian.columns = column_names
native = arrests_2016['American\nIndian or\nAlaska\nNative']
native.columns = column_names
hispan = arrests_2016['Hispanic\nor\nLatino']
hispan.columns = column_names

arrests_2016 = pd.DataFrame({'Race': ['White', 'Black', 'Asian', 'Native', 'Hispanic']})
arrests_2016['Number of Arrests'] = ''
arrests_2016['Number of Arrests'] = np.where(arrests_2016['Race'] == 'White', white['Number'],
                                             arrests_2016['Number of Arrests'])
arrests_2016['Number of Arrests'] = np.where(arrests_2016['Race'] == 'Black', black['Number'],
                                             arrests_2016['Number of Arrests'])
arrests_2016['Number of Arrests'] = np.where(arrests_2016['Race'] == 'Asian', asian['Number'],
                                             arrests_2016['Number of Arrests'])
arrests_2016['Number of Arrests'] = np.where(arrests_2016['Race'] == 'Native', native['Number'],
                                             arrests_2016['Number of Arrests'])
arrests_2016['Number of Arrests'] = np.where(arrests_2016['Race'] == 'Hispanic', hispan['Number'],
                                             arrests_2016['Number of Arrests'])

arrests_2016['Percent Arrests'] = ''
arrests_2016['Percent Arrests'] = np.where(arrests_2016['Race'] == 'White', white['Percent'],
                                           arrests_2016['Percent Arrests'])
arrests_2016['Percent Arrests'] = np.where(arrests_2016['Race'] == 'Black', black['Percent'],
                                           arrests_2016['Percent Arrests'])
arrests_2016['Percent Arrests'] = np.where(arrests_2016['Race'] == 'Asian', asian['Percent'],
                                           arrests_2016['Percent Arrests'])
arrests_2016['Percent Arrests'] = np.where(arrests_2016['Race'] == 'Native', native['Percent'],
                                           arrests_2016['Percent Arrests'])
arrests_2016['Percent Arrests'] = np.where(arrests_2016['Race'] == 'Hispanic', hispan['Percent'],
                                           arrests_2016['Percent Arrests'])

arrests_2016['Number of Arrests'] = arrests_2016['Number of Arrests'].astype(str).str.replace(',', '')
arrests_2016['Year'] = '2016'


# Build a new series of the number of arrests by race for 2017
# Note: Data on hispanic arrests isn't gathered by all agencies, hence percentages will not total 100
arrests_2017 = arrests_2017.loc[[2]]
column_names = ['Number', 'Percent']

white = arrests_2017['White']
white.columns = column_names
black = arrests_2017['Black or\nAfrican\nAmerican']
black.columns = column_names
asian = arrests_2017['Asian']
asian.columns = column_names
native = arrests_2017['American\nIndian or\nAlaska\nNative']
native.columns = column_names
hispan = arrests_2017['Hispanic\nor\nLatino']
hispan.columns = column_names

arrests_2017 = pd.DataFrame({'Race': ['White', 'Black', 'Asian', 'Native', 'Hispanic']})
arrests_2017['Number of Arrests'] = ''
arrests_2017['Number of Arrests'] = np.where(arrests_2017['Race'] == 'White', white['Number'],
                                             arrests_2017['Number of Arrests'])
arrests_2017['Number of Arrests'] = np.where(arrests_2017['Race'] == 'Black', black['Number'],
                                             arrests_2017['Number of Arrests'])
arrests_2017['Number of Arrests'] = np.where(arrests_2017['Race'] == 'Asian', asian['Number'],
                                             arrests_2017['Number of Arrests'])
arrests_2017['Number of Arrests'] = np.where(arrests_2017['Race'] == 'Native', native['Number'],
                                             arrests_2017['Number of Arrests'])
arrests_2017['Number of Arrests'] = np.where(arrests_2017['Race'] == 'Hispanic', hispan['Number'],
                                             arrests_2017['Number of Arrests'])

arrests_2017['Percent Arrests'] = ''
arrests_2017['Percent Arrests'] = np.where(arrests_2017['Race'] == 'White', white['Percent'],
                                           arrests_2017['Percent Arrests'])
arrests_2017['Percent Arrests'] = np.where(arrests_2017['Race'] == 'Black', black['Percent'],
                                           arrests_2017['Percent Arrests'])
arrests_2017['Percent Arrests'] = np.where(arrests_2017['Race'] == 'Asian', asian['Percent'],
                                           arrests_2017['Percent Arrests'])
arrests_2017['Percent Arrests'] = np.where(arrests_2017['Race'] == 'Native', native['Percent'],
                                           arrests_2017['Percent Arrests'])
arrests_2017['Percent Arrests'] = np.where(arrests_2017['Race'] == 'Hispanic', hispan['Percent'],
                                           arrests_2017['Percent Arrests'])

arrests_2017['Number of Arrests'] = arrests_2016['Number of Arrests'].astype(str).str.replace(',', '')
arrests_2017['Year'] = '2017'


# Join arrest data to race data
arrests = arrests_2015.append([arrests_2016, arrests_2017], ignore_index=True)
df_race = df_race.merge(arrests, on=['Race', 'Year'], how='left')


# Create new row for totals
df_race['Number of Deaths'] = df_race['Number of Deaths'].apply(pd.to_numeric, errors='coerce')
df_race['Number of Arrests'] = df_race['Number of Arrests'].apply(pd.to_numeric, errors='coerce')
df_race['Percent Arrests'] = df_race['Percent Arrests'].apply(pd.to_numeric, errors='coerce')

df_race = df_race.append(df_race[df_race['Year'] == '2015'].sum(numeric_only=True), ignore_index=True)
df_race['Race'] = np.where(df_race.isna(), 'Total', df_race)
df_race.at[16,'Armed'] = 'No'
df_race.at[16,'Year'] = '2015'

df_race = df_race.append(df_race[df_race['Year'] == '2016'].sum(numeric_only=True), ignore_index=True)
df_race['Race'] = np.where(df_race.isna(), 'Total', df_race)
df_race.at[17,'Armed'] = 'No'
df_race.at[17,'Year'] = '2016'

df_race = df_race.append(df_race[df_race['Year'] == '2017'].sum(numeric_only=True), ignore_index=True)
df_race['Race'] = np.where(df_race.isna(), 'Total', df_race)
df_race.at[18,'Armed'] = 'No'
df_race.at[18,'Year'] = '2017'


# Build a new column in race data for number killed per arrest
df_race['Deaths per Arrest'] = df_race['Number of Deaths']/df_race['Number of Arrests']
df_race['Deaths per 1,000,000 Arrests'] = df_race['Number of Deaths']/df_race['Number of Arrests']*1000000


# Visualize number killed by race per arrest, armed vs. unarmed
plt.figure(figsize=(10, 5))
bars = ['Total', 'White', 'Black', 'Hispanic', 'Asian', 'Native']
color = ['#570003', '#890105', '#b80006']

plot = sns.barplot(x='Race', y='Deaths per 1,000,000 Arrests', data=df_race, order=bars, palette=color, hue='Year')
plt.ylim(0,18)
plt.setp(plot.patches, linewidth=1)

font = {'fontname':'Helvetica'}
plt.title('Unarmed Fatal Police Shootings in the U.S. per 1,000,000 Arrests, 2015-2018',**font)
plt.xlabel('Race',**font)
plt.ylabel('Deaths per 1,000,000 Arrests',**font)
plt.xticks(**font)
plt.savefig('Unarmed Shootings per Arrest, 2015-2018.png')