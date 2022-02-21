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
merged_df['year'] = merged_df['date'].str[0:4]
merged_df.columns

df_inn1 = merged_df.loc[(merged_df["over"] < 6) & (merged_df["inning"] == 1)].groupby(['id',"date", "winner","inning", "batting_team", "year", "result"], as_index=False).agg({'total_runs': "sum"})
df_inn1.rename(columns={'batting_team':'inn1_team','total_runs':'inn1_runs'}, inplace=True)

df_inn2 = merged_df.loc[(merged_df["over"] < 6) & (merged_df["inning"] == 2)].groupby(['id',"date", "winner","inning", "batting_team", "year", "result"], as_index=False).agg({'total_runs': "sum"})
df_inn2.rename(columns={'batting_team':'inn2_team','total_runs':'inn2_runs'}, inplace=True)

uber_pd = pd.merge(df_inn1, df_inn2, on="id")
uber_pd.columns

uber_pd['pp_winner']= np.where(uber_pd['inn1_runs']>uber_pd['inn2_runs'],uber_pd['inn1_team'],uber_pd['inn2_team'])

uber_pd['pp_boom']= np.where(uber_pd['pp_winner'] == uber_pd['winner_x'],1,0)
uber_pd['pp_unboom_first']= np.where((uber_pd['pp_winner'] != uber_pd['winner_x']) & (uber_pd['inn1_runs']>uber_pd['inn2_runs']),1,0)
uber_pd['pp_unboom_second']= np.where((uber_pd['pp_winner'] != uber_pd['winner_x']) & (uber_pd['inn2_runs']>uber_pd['inn1_runs']),1,0)

uber_pd['first_team_won'] = np.where(uber_pd['result_x'] == 'runs',1,0)
uber_pd['second_team_won'] = np.where(uber_pd['result_x'] == 'wickets',1,0)

uber_pd['counter']=1

uber_pd = uber_pd.groupby(['year_x']).agg({'pp_boom': "sum", 'pp_unboom_first': "sum", 'pp_unboom_second': "sum", 'first_team_won': "sum", 'second_team_won': "sum",'counter': "sum"})
uber_pd['pp_boom_perc'] = uber_pd['pp_boom']*100/uber_pd['counter']
uber_pd['chaser_win_perc'] = uber_pd['second_team_won']*100/uber_pd['counter']
uber_pd.head
##########################
#pp_superiority_count = uber_pd['pp_boom'].sum()
#total_matches_count = uber_pd['counter'].sum()
#pp_failure_count = total_matches_count - pp_superiority_count
#print("All IPL matches in 2008")
#print("Powerplay wins : ", pp_superiority_count)
#print("Total number of matches : ", total_matches_count)
#y = np.array([pp_superiority_count, pp_failure_count])
#mylabels = ["PP Winners winning match", "PP winners losing match"]
#myexplode = [0.05, 0.05]

#plt.pie(y, labels = mylabels, explode = myexplode)
#plt.show() 
