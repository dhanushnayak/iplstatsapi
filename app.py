from fastapi import FastAPI
import uvicorn
from api.batsman_api import bat
from api.players_api import player
from api.bowler_api import bowl
version = "0.1"
app =  FastAPI()

app.include_router(player)
app.include_router(bat)
app.include_router(bowl)

@app.api_route("/",tags=['Index'])
def index():
    global version
    return {"Version": f'{version}',"author":"Dhanush","email":"dhanushnayak.pythonnotebook@gmail.com"}
if __name__=='__main__': uvicorn.run(app=app,host="0.0.0.0",port=8000)