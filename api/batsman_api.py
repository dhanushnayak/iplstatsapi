from typing import List,Union
from pydantic import BaseModel
import code.batsman as data_fetch
from fastapi import FastAPI,APIRouter,requests,Depends
bat = APIRouter(prefix='/api/batsman',tags=['batsman_data'])

class player_list(BaseModel):
    player:List[str]

async def common_parameters(
     limit: int = 10, start_year: int = 2008, end_year: int=2020,required: str="score"
     ):
    return {"limit": limit,'start_year':start_year,"end_year":end_year,'required':required}


@bat.api_route('/compare/',methods=["POST"])
def get_compare_of_player(players: player_list,commons: dict = Depends(common_parameters)):
    data = data_fetch.get_score(players=players.dict()['player'],start_year=commons.get('start_year'),end_year=commons.get('end_year'),required=commons.get('required'))
    return {"data":data.to_json()}

@bat.get("/details")
def get_details(player):
    data = data_fetch.get_detail(player)
    return {"data":data}

@bat.api_route('/outs',methods=['GET'])
def get_to_wicket_dismilled(player,limit:int=10):
    data = data_fetch.get_top_wicket_dismilled(player=player,limit=limit)
    return {"data":data.to_json()}


@bat.api_route('/wickettakers',methods=['GET'])
def top_wicket_taker_of_batsman(player,limit:int=10):
    data = data_fetch.get_top_wicket_taker_of_batsman(player,limit=limit)
    return {"data":data.to_json()}

@bat.api_route('/scores/team',methods=['GET'])
def get_score_on_team(player,limit:int=10):
    data = data_fetch.get_score_on_team(player=player,focus="batting",limit=limit)
    return {"data":data.to_json()}

@bat.api_route('/scores/bowler',methods=['GET'])
def get_score_on_bowler(player,limit:int=10):
    data = data_fetch.get_score_on_bowler(player=player,limit=limit)
    return {"data":data.to_json()}

@bat.get("/strikes/team")
def get_strikes_on_team(player,limit:int=10):
    data = data_fetch.get_strikes_on_team(player=player,limit=limit)
    return {"data":data.to_json()}

@bat.get("/strikes/year")
def get_strikes_by_year(player,limit:int=10):
    data = data_fetch.get_strikes_by_year(player,limit=limit)
    return {"data":data.to_json()}

@bat.get("/strikes/bowler")
def get_strikes_by_year(player,limit:int=10):
    data = data_fetch.get_strikes_on_bowler(player,limit=limit)
    return {"data":data.to_json()}