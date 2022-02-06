import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

pd.set_option('display.max_rows', 1000)
df= pd.read_csv("/kaggle/input/ipl-complete-dataset-20082020/IPL Ball-by-Ball 2008-2020.csv")
df_m = pd.read_csv("/kaggle/input/ipl-complete-dataset-20082020/IPL Matches 2008-2020.csv")

merged_df = pd.merge(df, df_m, on="id")
merged_df.columns

df_inn1 = merged_df.loc[(merged_df["over"] < 6) & (merged_df["inning"] == 1)].groupby(['id',"date", "winner","inning", "batting_team"], as_index=False).agg({'batsman_runs': "sum"})
df_inn1.rename(columns={'batting_team':'inn1_team','batsman_runs':'inn1_runs'}, inplace=True)


df_inn2 = merged_df.loc[(merged_df["over"] < 6) & (merged_df["inning"] == 2)].groupby(['id',"date", "winner","inning", "batting_team"], as_index=False).agg({'batsman_runs': "sum"})
df_inn2.rename(columns={'batting_team':'inn2_team','batsman_runs':'inn2_runs'}, inplace=True)

uber_pd = pd.merge(df_inn1, df_inn2, on="id")

uber_pd['pp_winner']= np.where(uber_pd['inn1_runs']>uber_pd['inn2_runs'],uber_pd['inn1_team'],uber_pd['inn2_team'])

uber_pd['pp_boom']= np.where(uber_pd['pp_winner'] == uber_pd['winner_x'],1,0)

uber_pd['pp_boom_batting_first'] = np.where((uber_pd['pp_winner'] == uber_pd['winner_x']) & (uber_pd['pp_winner'] == uber_pd['inn1_team']),1,0)
uber_pd['pp_boom_batting_second'] = np.where((uber_pd['pp_winner'] == uber_pd['winner_x']) & (uber_pd['pp_winner'] == uber_pd['inn2_team']),1,0)

uber_pd['pp_unboom_batting_first'] = np.where((uber_pd['pp_winner'] != uber_pd['winner_x']) & (uber_pd['pp_winner'] == uber_pd['inn1_team']),1,0)
uber_pd['pp_unboom_batting_second'] = np.where((uber_pd['pp_winner'] != uber_pd['winner_x']) & (uber_pd['pp_winner'] == uber_pd['inn2_team']),1,0)

uber_pd['counter']=1

pp_superiority_count = uber_pd['pp_boom'].sum()
total_matches_count = uber_pd['counter'].sum()
pp_failure_count = total_matches_count - pp_superiority_count

count_pp_boom_batting_first = uber_pd['pp_boom_batting_first'].sum()
count_pp_boom_batting_second = uber_pd['pp_boom_batting_second'].sum()

count_pp_unboom_batting_first = uber_pd['pp_unboom_batting_first'].sum()
count_pp_unboom_batting_second = uber_pd['pp_unboom_batting_second'].sum()

print("All IPL matches from 2008-2020")
print("Powerplay wins : ", pp_superiority_count)
print("Total number of matches : ", total_matches_count)
print('Powerplay champs winning match while batting first : ', count_pp_boom_batting_first)
print('Powerplay champs winning match while batting second : ', count_pp_boom_batting_second)
print('Powerplay champs losing match while batting first : ', count_pp_unboom_batting_first)
print('Powerplay champs losing match while batting second : ', count_pp_unboom_batting_second)

y = np.array([pp_superiority_count, pp_failure_count])
mylabels = ["PP Winners winning match", "PP winners losing match"]
myexplode = [0.05, 0.05]

plt.pie(y, labels = mylabels, explode = myexplode)
plt.show() 

#uber_pd.head()
#uber_pd.to_csv('/kaggle/working/out2.csv')

###############################
#df2 = df.groupby(['batsman']).agg({"batsman_runs": "sum", "id": "nunique"})
#df3 = df.groupby('batsman').count()
#df2.columns
#df2.head()
#print(df2[['batsman_runs']])
#df3 = df.loc[df["batsman_runs"] == 6].groupby('batsman').agg({'batsman_runs': "count"})
#df3.head()
