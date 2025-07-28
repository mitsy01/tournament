from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlalchemy_uri: str = "mysql+aiomysql://localhost:5432/tournament"
    secret_key: str = "secret key"
    exp_time_minutes: int = 30
    
    model_config = SettingsConfigDict(env_file=".env")
    
    
settings = Settings()
