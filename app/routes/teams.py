from fastapi import APIRouter


from app.db.teams import db_actions


teams_router = APIRouter(prefix="/teams", tags=["Team"])
