from api.batsman_api import player_list
import code.player as data_fetch
from fastapi import FastAPI,APIRouter,requests,Depends
player = APIRouter(prefix='/api',tags=['players_data'])

@player.get("/player")
def get_player():
    names = data_fetch.get_players_names()
    return {"names":names}

@player.post("/ahead")
def get_ahead(batsman:str,bowler:str):
    data = data_fetch.get_head_on(batsman=batsman,bowler=bowler)
    return {"data":data}

@player.get("/images")
def get_images_data(name):
    data = data_fetch.get_images_data(name)
    return {"data":data}