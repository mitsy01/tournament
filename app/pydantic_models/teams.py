from pydantic import BaseModel


class TeamModel(BaseModel):
    name: str
    private: bool
    

class TeamModelResponce(TeamModel):
    id: str
    
    