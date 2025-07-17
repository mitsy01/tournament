from pydantic import BaseModel


class TeamModel(BaseModel):
    name_team: str
    private: bool
    

class TeamModelResponce(TeamModel):
    id: str
    
    