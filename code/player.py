import pandas as pd
import numpy as np
import os
from warnings import filterwarnings
from .utilities.utils import convert_to_over,nan_check
base_dir='/'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
path = os.path.join(base_dir,'./data/data.csv')
images_path = os.path.join(base_dir,"./data/images.csv")
filterwarnings('ignore')

data = pd.read_csv(path)
image_data = pd.read_csv(images_path)

wickets_form = ['caught', 'bowled', 'lbw', 'stumped',
       'caught and bowled', 'hit wicket']
extras_form=['byes', 'wides', 'legbyes', 'noballs', 'penalty']

def get_players_names():
    global data
    batsman = data['batsman'].unique()
    bowler = data['bowler'].unique()
    name =  list(batsman)
    name.extend(list(bowler))
    name = list(set(name))
    return name


def get_head_on(batsman,bowler):
    global data
    global wickets_form
    player_1 = batsman
    player_2 = bowler
    bdf=data[(data['batsman'].str.contains(player_1)) & (data['bowler'].str.contains(player_2))]
    matchs = bdf['id'].nunique() if bdf.shape[0]>0 else 0
    number_of_balls = bdf.shape[0] if bdf.shape[0]>0 else 0
    batsman_score = bdf['batsman_runs'].sum() 
    wicket_taken = bdf[(bdf['is_wicket']==1) & (bdf['dismissal_kind'].isin(wickets_form))]['id'].count() 
    p1 = bdf[bdf['over'].isin(range(0,7))] 
    p2 = bdf[bdf['over'].isin(range(7,16))] 
    p3 = bdf[bdf['over'].isin(range(16,20))] 
    score_in_overs = {"powerplay_over":int(p1['batsman_runs'].sum()) ,"middle_over":int(p2['batsman_runs'].sum()) ,"end_overs":int(p3['batsman_runs'].sum()) }
    strike_in_overs = {"powerplay_over":round((p1['batsman_runs'].sum()/len(p1))*100,3) ,
                        "middle_over":round((p2['batsman_runs'].sum()/len(p2))*100,3) ,
                        "end_overs":round((p3['batsman_runs'].sum()/len(p3))*100,3) }
    outs_in_overs = {"powerplay_over":int(bdf[(bdf['player_dismissed']==player_1) & (bdf['over'].isin(range(0,7))) & (bdf['dismissal_kind'].isin(wickets_form))]['is_wicket'].sum()) ,
                        "middle_over":int(bdf[(bdf['player_dismissed']==player_1) & (bdf['over'].isin(range(7,16))) & (bdf['dismissal_kind'].isin(wickets_form))]['is_wicket'].sum()) ,
                        "death_over":int(bdf[(bdf['player_dismissed']==player_1) & (bdf['over'].isin(range(16,20))) & (bdf['dismissal_kind'].isin(wickets_form))]['is_wicket'].sum()) }
    eco_in_overs = {"powerplay_over":round(p1['total_runs'].sum()/convert_to_over(len(p1)),3) ,
                    "middle_over":round(p2['total_runs'].sum()/convert_to_over(len(p2)),3) ,
                    "death_over":round(p3['total_runs'].sum()/convert_to_over(len(p3)),3) 
                }
    balls_score=bdf.groupby(['total_runs']).count()['id'].to_dict() 
    avg_eco = round(batsman_score/convert_to_over(number_of_balls),3) 
    strike_rate=round((batsman_score/number_of_balls)*100,3) 
    score_on_year=bdf.groupby('year')['batsman_runs'].sum() 
    score_by_year={}
    wicket_on_year=bdf[(bdf['player_dismissed']==player_1) &  (bdf['dismissal_kind'].isin(wickets_form))].groupby('year')['id'].count() 
    wicket_by_year={}
    for i in range(2008,2020): 
        try: score_by_year[i] = int(score_on_year[i])
        except: score_by_year[i] = 0
        try: wicket_by_year[i] = int(wicket_on_year[i])
        except:   wicket_by_year[i] = 0

    data_to_return = {"matchs":nan_check(int(matchs)),
                       "runs":nan_check(int(batsman_score)),
                       "balls":nan_check(int(number_of_balls)),
                       "wickets_fall":nan_check(int(wicket_taken)),
                       "4s":nan_check(int(balls_score.get(4,0))),
                       "6s":nan_check(int(balls_score.get(6,0))),
                       "dots":nan_check(int(balls_score.get(0,0))),
                       "strike_rate":nan_check(float(strike_rate)),
                       "average_economy":nan_check(float(avg_eco)),
                       "score_by_overs":nan_check(score_in_overs),
                       "strike_rate_by_over":nan_check(strike_in_overs),
                       "economy_by_over":nan_check(eco_in_overs),
                       "outs_by_over":nan_check(outs_in_overs),
                       "score_by_year":nan_check(score_by_year),
                       "wicket_by_year":nan_check(wicket_by_year)             
                    }
    return data_to_return

def get_images_data(player_name):
    global image_data
    return image_data[image_data['name']==player_name]['image'].values[0]