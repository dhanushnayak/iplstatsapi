from typing import List,Union
from pydantic import BaseModel
import code.bowler as data_fetch
import json
from fastapi import FastAPI,APIRouter,requests,Depends
bowl = APIRouter(prefix='/api/bowler',tags=['bowler_data'])

class player_list(BaseModel):
    player:List[str]


async def common_parameters(
     limit: int = 10, start_year: int = 2008, end_year: int=2020, required: str="wickets"
     ):
    return {"limit": limit,'start_year':start_year,"end_year":end_year,"required":required}


@bowl.api_route('/compare/',methods=["POST"])
def get_compare_of_player(players: player_list,commons: dict = Depends(common_parameters)):
    data = data_fetch.get_stats(players=players.dict()['player'],start_year=commons.get('start_year'),end_year=commons.get('end_year'),required=commons.get("required"))
    return {"data":data.to_json()}


@bowl.get("/details")
def get_details(player):
    data = data_fetch.get_detail(player)
    return {"data":data}

@bowl.api_route('/wickets/team',methods=["GET"])
def get_player_wickets_stats_on_team(player,limit:int=10):
    data = data_fetch.get_player_wickets_stats_on_team(player,limit=limit)
    return {"data":data.to_json()}



@bowl.api_route('/wickets/batsman',methods=["GET"])
def get_player_top_wickets_on_batsman(player,limit:int=10):
    data = data_fetch.get_player_top_wickets_on_batsman(player,limit=limit)
    return {"data":data.to_json()}

@bowl.get('/wickets/year')
def get_total_wickets_on_year(player):
    data = data_fetch.get_total_wickets_on_year(player)
    return {"data":data.to_json()}

@bowl.api_route('/wickets/dismisstype',methods=["GET"])
def get_player_top_wickets_form(player,limit: int =10):
    data = data_fetch.get_player_top_wickets_form(player=player,limit=limit)
    return {"data":data.to_json()}

@bowl.get('/economy/year')
def get_economy_of_bowler_on_year(player):
    data = data_fetch.get_economy_of_bowler_on_year(player)
    return {"data":data.to_json()}


@bowl.get('/economy/team')
def get_player_economy_on_teams(player,limit: int=10):
    data = data_fetch.get_player_economy_on_teams(player,limit=limit)
    return {"data":data.to_json()}

@bowl.get('/economy/player')
def get_player_economy_on_player(player,limit: int=10):
    data = data_fetch.get_player_economy_on_player(player,limit=limit)
    return {"data":data.to_json()}

@bowl.get('/extras')
def get_player_extras(player):
    data = data_fetch.get_extras(player)
    return {"data":data.to_json()}