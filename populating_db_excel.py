import pandas as pd

# From an Excel backup file, will convert to a SQL script
df = pd.read_excel('~/Documents/series_backup.xlsx')

# Creating two dataframes
flag = df.finished == False

""" NOTE: This is possible only because previously, the Excel file is organized first showing ongoing  and 
then the finished series"""

df_finished = df[~flag].reset_index()
df_ongoing = df[flag].reset_index()


# First, doing the finished series
series = []

for i in range(len(df_finished)):
    series.append(df_finished['name'][i])

# series is the table name that I chose for my database
sql_script_finished = 'INSERT INTO series(name, finished) VALUES '

for i in range(len(df_finished)):
    sql_script_finished += '('
    sql_script_finished += f"'{series[i]}', "
    sql_script_finished += "'true'), "
    sql_script_finished += '\n'

# Doing '-3' you will delete the '\n' character and ', '
sql_script_finished = sql_script_finished[:-3]
sql_script_finished += ';'


# Now, the ongoing series
name = []
season = []
episode = []

for i in range(len(df_ongoing)):
    name.append(df['name'][i])
    season.append(int(df['season'][i]))
    episode.append(int(df['episode'][i]))

sql_script_ongoing = 'INSERT INTO series(name, season, episode, finished) VALUES '

for i in range(len(df_ongoing)):
    sql_script_ongoing += '('
    sql_script_ongoing += f"'{name[i]}', "
    sql_script_ongoing += f"{season[i]}, "
    sql_script_ongoing += f"{episode[i]}, "
    sql_script_ongoing += "'false'), "
    sql_script_ongoing += '\n'
    
sql_script_ongoing = sql_script_ongoing[:-3]
sql_script_ongoing += ';'

print("Script para Finished series:\n")
print(sql_script_finished)
print()
print("\nScript para Ongoing series:\n")
print(sql_script_ongoing)
