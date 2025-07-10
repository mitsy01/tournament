from pydantic import BaseModel 


class TokenModel(BaseModel):
    acces_token: str
    token_type: str = "Bearer"