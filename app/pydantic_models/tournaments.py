from datetime import date


from pydantic import BaseModel, Field


from app.db.tournaments.db_actions import Vote
from app.db.teams.models import Team
from app.db.tournaments.models import Tournament


class TournamentModel(BaseModel):
    name_tourna: str = Field(...)
    expire_date: int = Field(7)
    
    
class TournamentModelResponce(TournamentModel):
    id: str
    expire_date:date
    
    
class VoteModel(BaseModel):
    team_id: str
    tournament_id: str
    vote: Vote
    

class ResultModel(BaseModel):
    team_name: str
    tournament_name: str
    result: float
    vote_result: int