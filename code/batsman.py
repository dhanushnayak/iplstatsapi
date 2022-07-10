import pandas as pd
import numpy as np
import os
from warnings import filterwarnings
from .player import data
filterwarnings('ignore')

def get_score(**kwargs):
        global data
        players = kwargs.get('players',None)
        start_year = kwargs.get('start_year',2008)
        end_year = kwargs.get('end_year',2020)
        method=kwargs.get("required","score")
        if players is not None:
            if isinstance(players,str):
                if method=="score":checkdf = get_score_by_year(players)
                if method=='strike':checkdf = get_strikes_by_year(players,top=False)
                data1 = []
                for year in range(2008,2021):
                    d={}
                    d['year']=year
                    try:d[players]=checkdf.loc[year].values[0]
                    except: d[players]=0
                    data1.append(d)
                dataframe =  pd.DataFrame(data1).set_index('year')
                if start_year is not None:dataframe = dataframe.loc[start_year:]
                if end_year is not None: dataframe = dataframe.loc[:end_year]
                del data1
                return dataframe

            if isinstance(players,list):
                l=[]
                for player in players: 
                    #checkdf = data[data['batsman'].str.contains(player)][['batsman_runs','year']].groupby('year').sum()
                    if method=="score":checkdf = get_score_by_year(player)
                    if method=='strike':checkdf = get_strikes_by_year(player,top=False)
                    data1 = []
                    for year in range(2008,2021):
                        d={}
                        d['year']=year
                        try:d[player]=checkdf.loc[year]
                        except: d[player]=0
                        data1.append(d)
                    dataframe =  pd.DataFrame(data1).set_index('year')
                    del data1
                    if start_year is not None:dataframe = dataframe.loc[start_year:]
                    if end_year is not None: dataframe = dataframe.loc[:end_year]     
                    l.append(dataframe)
                return pd.concat(l,axis=1)


def get_top_wicket_taker_of_batsman(player,limit=10):
        global data
        return data[(data['batsman']==player)&(data['is_wicket']==1) & (data['player_dismissed']==player)].loc[:,['bowler','dismissal_kind']].groupby('bowler').count().nlargest(columns='dismissal_kind',n=limit).loc[:,'dismissal_kind']

def get_top_wicket_dismilled(player,limit=10):
        global data
        return data[(data['batsman']==player)&(data['is_wicket']==1) & (data['player_dismissed']==player)].loc[:,['bowler','dismissal_kind']].groupby('dismissal_kind').count().nlargest(columns='bowler',n=limit).loc[:,'bowler']

def get_score_on_bowler(player,limit=10,top=True,low=False):
        global data
        batdf=data[data['batsman'].str.contains(player)]
        data_df = batdf[batdf['is_wicket']==0].groupby('bowler')['batsman_runs'].sum()
        if top: return data_df.nlargest(limit)
        if low: return data_df.nsmallest(limit)
        else: return data_df

def get_score_on_team(player,focus='batting',limit=10):
        global data
        if focus=='batting':
            batdf=data[data['batsman'].str.contains(player)]
            return batdf.groupby(['bowling_team'])['batsman_runs'].sum().nlargest(limit)
        if focus=='bowling':
            return data[data['bowler'].str.contains(player)].groupby(['batting_team'])['is_wicket'].sum().nlargest(limit)

def get_score_by_year(player):
    global data
    return data[data['batsman'].str.contains(player)][['batsman_runs','year']].groupby('year').sum().loc[:,'batsman_runs']


def get_strikes_on_team(player,limit=10,top=True,low=False):
    bdf = data[data['batsman'].str.contains(player)]
    balls=bdf.groupby('bowling_team')['ball'].count()
    score = bdf.groupby('bowling_team')['batsman_runs'].sum()
    data_df = ((score/balls)*100)
    if top: return data_df.sort_values(ascending=False).apply(lambda x: round(x,3)).iloc[:limit]
    if low: return data_df.sort_values(ascending=True).apply(lambda x: round(x,3)).iloc[:limit]
    else: return data_df.apply(lambda x: round(x,3))

def get_strikes_by_year(player,limit=10, top=True,low=False):
    bdf = data[data['batsman'].str.contains(player)]
    balls=bdf.groupby('year')['ball'].count()
    score = bdf.groupby('year')['batsman_runs'].sum()
    data_df = ((score/balls)*100)
    if top: return data_df.sort_values(ascending=False).apply(lambda x: round(x,3)).iloc[:limit]
    if low: return data_df.sort_values(ascending=True).apply(lambda x: round(x,3)).iloc[:limit]
    else: return data_df.apply(lambda x: round(x,3))

def get_strikes_on_bowler(player,limit=10, top=True,low=False):
    bdf = data[data['batsman'].str.contains(player)]
    balls=bdf.groupby('bowler')['ball'].count()
    score = bdf.groupby('bowler')['batsman_runs'].sum()
    data_df = ((score/balls)*100)
    if top: return data_df.sort_values(ascending=False).apply(lambda x: round(x,3)).iloc[:limit]
    if low: return data_df.sort_values(ascending=True).apply(lambda x: round(x,3)).iloc[:limit]
    else: return data_df.apply(lambda x: round(x,3))


def get_detail(player):
    bdf=data[data['batsman'].str.contains(player)]
    matchs=bdf['id'].nunique()
    total_score=bdf['batsman_runs'].sum()
    avg_strike=round((total_score/bdf.shape[0])*100,3)
    runs_cate=bdf.groupby('batsman_runs')['batsman'].count().to_dict()
    highest = bdf.groupby('id')['batsman_runs'].sum().nlargest(1).values[0]
    highest_score_in_season = bdf.groupby('year')['batsman_runs'].sum().nlargest(1).values[0]
    wickets_fallen = bdf[(bdf['player_dismissed']==player)]['is_wicket'].sum()
    number_of_notout_matchs = bdf.id.nunique()-wickets_fallen
    best_patner = bdf.groupby(['id','non_striker'])['batsman'].count().nlargest(1).index[0][1]
    number_30 = bdf.groupby('id')['batsman_runs'].sum().apply(lambda x: np.where(x in range(30,50),1,0)).sum()
    number_50 = bdf.groupby('id')['batsman_runs'].sum().apply(lambda x: np.where(x in range(50,100),1,0)).sum()
    number_100 = bdf.groupby('id')['batsman_runs'].sum().apply(lambda x: np.where(x in range(100,150),1,0)).sum()
    number_150 = bdf.groupby('id')['batsman_runs'].sum().apply(lambda x: np.where(x in range(150,200),1,0)).sum()
    number_200 = bdf.groupby('id')['batsman_runs'].sum().apply(lambda x: np.where(x in range(200,250),1,0)).sum()
    p1 = bdf[bdf['over'].isin(range(0,7))]
    p2 = bdf[bdf['over'].isin(range(7,16))]
    p3 = bdf[bdf['over'].isin(range(16,20))]
    score_in_overs = {"powerplay_over":int(p1['batsman_runs'].sum()),"middle_over":int(p2['batsman_runs'].sum()),"end_overs":int(p3['batsman_runs'].sum())}
    strike_in_overs = {"powerplay_over":round((p1['batsman_runs'].sum()/len(p1))*100,3),
                    "middle_over":round((p2['batsman_runs'].sum()/len(p2))*100,3),
                    "end_overs":round((p3['batsman_runs'].sum()/len(p3))*100,3)}
    outs_in_overs = {"powerplay_over":int(bdf[(bdf['player_dismissed']==player) & (bdf['over'].isin(range(0,7)))]['is_wicket'].sum()),
                    "middle_over":int(bdf[(bdf['player_dismissed']==player) & (bdf['over'].isin(range(7,16)))]['is_wicket'].sum()),
                    "death_over":int(bdf[(bdf['player_dismissed']==player) & (bdf['over'].isin(range(16,20)))]['is_wicket'].sum())}
    data_to_return ={
        "match":int(matchs),"total_runs":int(total_score),"average_strike":round(avg_strike,3),
        "highest_score":int(highest),"highest_score_in_season":int(highest_score_in_season),
        "4s":int(runs_cate.get(4)),"6s":int(runs_cate.get(6)),"30s":int(number_30),"50s":int(number_50),"100s":int(number_100),"150s":int(number_150),"200s":int(number_200),
        "out_matchs":int(wickets_fallen),"notout_matchs":int(number_of_notout_matchs),"balls_played":len(bdf),"best_patner":str(best_patner),
        "scores_in_overs":score_in_overs,"strikes_in_overs":strike_in_overs,"outs_in_overs":outs_in_overs
    }
    return data_to_return