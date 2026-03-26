from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from sqlmodel import Session, select
from models import Bio, Stats, engine


app = FastAPI()


    
# Endpoint to get all players for selection
@app.get("/players")
def get_players():
    with Session(engine) as session:
        players = session.exec(select(Bio)).all()
        return [
            {"id": player.id, "name": f"{player.FirstName} {player.LastName}"}
            for player in players
        ]
    
app.mount("/", StaticFiles(directory="static", html=True), name="static")