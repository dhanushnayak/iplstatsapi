
import pandas as pd
import numpy as np
import os
from warnings import filterwarnings
filterwarnings('ignore')
from .utilities.utils import convert_to_over
from .player import data,wickets_form,extras_form


def get_stats(**kwargs):
        global data
        global wickets_form
        players = kwargs.get('players',None)
        method = kwargs.get('required','wickets')
        start_year = kwargs.get('start_year',2008)
        end_year = kwargs.get('end_year',2020)
        if players is not None:
            if isinstance(players,str):
                if method in ['wickets','economy']:
                    if method=='wickets':checkdf = get_total_wickets_on_year(players)
                    if method=='economy': checkdf = get_economy_of_bowler_on_year(players)
                    data1 = []
                    for year in range(2008,2021):
                        d={}
                        d['year']=year
                        try:d[players]=checkdf.loc[year]#.values[0]
                        except: d[players]=0
                        data1.append(d)
                    dataframe =  pd.DataFrame(data1).set_index('year')
                    if start_year is not None:dataframe = dataframe.loc[start_year:]
                    if end_year is not None: dataframe = dataframe.loc[:end_year]
                    del data1
                    return dataframe
                if method == "extras":
                    global extras_form
                    checkdf = get_extras(players)
                    d={}
                    for extra in extras_form:
                        try:d[extra] = checkdf[extra]
                        except:d[extra]=0
                    dataframe = pd.DataFrame(d)
                    return dataframe

            if isinstance(players,list):
                l=[]
                for player in players:
                    if method in ['wickets','economy']:
                        if method=='wickets':checkdf = get_total_wickets_on_year(player)
                        if method=='economy': checkdf = get_economy_of_bowler_on_year(player)
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
                    if method=='extras':
                        checkdf = get_extras(player)
                        data1 = []
                        for num,extra in enumerate(extras_form):
                            d={}
                            d['type']=extra
                            try:d[player] = checkdf[extra]
                            except:d[player]=0
                            data1.append(d)
                        dataframe =  pd.DataFrame(data1).set_index('type')
                        l.append(dataframe)
                return pd.concat(l,axis=1)

def get_player_wickets_stats_on_team(player,limit=10):
    global data
    global wickets_form
    dfb=data[data['bowler'].str.contains(player)]
    return dfb[(dfb['is_wicket']==1 ) & (dfb['dismissal_kind'].isin(wickets_form))].groupby('batting_team').count()['id'].sort_values(ascending=False).iloc[:limit]


def get_player_top_wickets_on_batsman(player,limit=10):
    global data
    global wickets_form
    dfb=data[data['bowler'].str.contains(player)]
    return dfb[(dfb['is_wicket']==1 ) & (dfb['dismissal_kind'].isin(wickets_form))].groupby('batsman').count()['id'].sort_values(ascending=False).iloc[:limit]


def get_player_top_wickets_form(player,limit=10):
    global data
    global wickets_form
    dfb=data[data['bowler'].str.contains(player)]
    return dfb[(dfb['is_wicket']==1 ) & (dfb['dismissal_kind'].isin(wickets_form))].groupby('dismissal_kind').count()['id'].sort_values(ascending=False).iloc[:limit]


def get_total_wickets_on_year(player):
    global data
    global wickets_form
    dfb=data[data['bowler'].str.contains(player)]
    checkdf = dfb[(dfb['is_wicket']==1 ) & (dfb['dismissal_kind'].isin(wickets_form))].groupby(['year']).count()['id']
    return checkdf

def get_economy_of_bowler_on_year(player):
    global data
    dfb = data[data['bowler'].str.contains(player)]
    score = dfb.groupby('id')['total_runs'].sum()
    ball = dfb.groupby('id')['ball'].count().apply(lambda x: convert_to_over(x))
    year = data[['id','year']].set_index('id')
    eco = pd.DataFrame(score/ball).rename(columns={0:'eco'})
    checkdf = pd.merge_asof(eco,year,on='id').groupby(['year']).mean()['eco'].apply(lambda x: round(x,3))
    return checkdf


def get_player_economy_on_teams(player,limit=10):
    global data
    dfb = data[data['bowler'].str.contains(player)]
    grpdata=dfb.groupby('batting_team')
    runs=grpdata['total_runs'].sum()
    overs = grpdata['ball'].count().apply(lambda x: convert_to_over(x))
    return (runs/overs).apply(lambda x: round(x,3)).sort_values(ascending=False).iloc[:limit]

def get_player_economy_on_player(player,limit=10,top=True,low=False):
    global data
    dfb = data[data['bowler'].str.contains(player)]
    grpdata=dfb.groupby('batsman')
    runs=grpdata['total_runs'].sum()
    overs = grpdata['ball'].count().apply(lambda x: convert_to_over(x))
    data_df = (runs/overs).apply(lambda x: np.where(x==np.inf,0,round(x,3))).dropna()
    if top: return data_df.sort_values(ascending=False).iloc[:limit]
    if low: return data_df.sort_values(ascending=True).iloc[:limit]
    else: return data_df
    
def get_extras(player):
    global data
    dfb = data[data['bowler'].str.contains(player)]
    return dfb[(dfb['extra_runs']>0)][['extra_runs','extras_type']].groupby('extras_type').sum()['extra_runs'].sort_values(ascending=False)

def get_detail(player):
    global data
    dfb = data[data['bowler'].str.contains(player)]
    num_overs=dfb.groupby('id').count()['ball'].apply(lambda x: convert_to_over(x)).sum()
    num_matchs=len(dfb.groupby('id').count())
    number_of_matchs_ball_coverage=dfb.groupby('id').count()['ball'].apply(lambda x: x%6).value_counts()
    number_of_matchs_over_completed=number_of_matchs_ball_coverage.loc[0]
    number_of_matchs_over_not_completed=number_of_matchs_ball_coverage[number_of_matchs_ball_coverage.index != 0].sum()
    number_of_balls=dfb.shape[0]
    balls_grp=dfb.groupby(['total_runs']).count()['id'].to_dict()
    total_runs=dfb['total_runs'].sum()
    avg_eco = round((total_runs/num_overs),3)
    p1=dfb[dfb['over'].isin(range(0,7))]
    p2=dfb[dfb['over'].isin(range(7,16))]
    p3=dfb[dfb['over'].isin(range(16,20))]
    wickets_in_overs = {"powerplay_over":int(p1[(p1['is_wicket']==1) & p1['dismissal_kind'].isin(wickets_form)]['id'].count()),
                        "middle_over":int(p2[(p2['is_wicket']==1) & p2['dismissal_kind'].isin(wickets_form)]['id'].count()),
                        "death_over":int(p3[(p3['is_wicket']==1) & p3['dismissal_kind'].isin(wickets_form)]['id'].count()),
                       }
    score_in_overs = {"powerplay_over":int(p1['total_runs'].sum()),"middle_over":int(p2['total_runs'].sum()),"death_over":int(p3['total_runs'].sum())}
    eco_in_overs ={"powerplay_over":round(p1['total_runs'].sum()/convert_to_over(len(p1)),3),"middle_over":round(p2['total_runs'].sum()/convert_to_over(len(p2)),3),"death_over":round(p3['total_runs'].sum()/convert_to_over(len(p3)),3)}
    total_wickets=dfb[(dfb['is_wicket'] & dfb['dismissal_kind'].isin(wickets_form))]['is_wicket'].sum()
    wickets_number = dfb[(dfb['is_wicket'] & dfb['dismissal_kind'].isin(wickets_form))].groupby('id')['is_wicket'].sum().value_counts().astype('int').to_dict()
    data_to_return = {"matchs":int(num_matchs),"overs":int(num_overs),"wickets":int(total_wickets),'balls':int(number_of_balls),"Avg_Economy":avg_eco,"runs":int(total_runs),
                    "dots":int(balls_grp.get(0)),"4s":int(balls_grp.get(4)),"6s":int(balls_grp.get(6)),"over_completed_matchs":int(number_of_matchs_over_completed),"over_not_completed_matchs":int(number_of_matchs_over_not_completed),
                    "wickets_data":wickets_number,"score_in_over":score_in_overs,"economy_in_over":eco_in_overs,"wickets_in_over":wickets_in_overs}
    return data_to_return

