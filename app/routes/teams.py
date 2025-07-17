from typing import Optional, List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.teams import db_actions
from app.routes.users import get_user_id
from app.pydantic_models.teams import TeamModel, TeamModelResponce
from app.db.base import get_db


teams_router = APIRouter(prefix="/teams", tags=["Team"])


@teams_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_team(
    user_id: Annotated[str, Depends(get_user_id)], 
    team_model: TeamModel,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await db_actions.create_team(user_id=user_id, team_model=team_model, db=db)
    
    
@teams_router.get("/{team_id}/")
async def get_team(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
    team_id: str = Path(..., description="Id команди")
):
    team =  await db_actions.get_team(team_id=team_id, db=db)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такої команди не існує.")
    return team


@teams_router.get("/", status_code=status.HTTP_202_ACCEPTED, response_model=List[TeamModelResponce])
async def get_teams(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
    private: Optional[bool] = Query(None)
):
    return await db_actions.get_teams(private=private, db=db)


@teams_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def del_team(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
    team_id: str = Path(...)
) -> None:
    result = await db_actions.del_team(team_id=team_id, user_id=user_id, db=db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    

@teams_router.post("/{team_id}/", status_code=status.HTTP_202_ACCEPTED)
async def add_user_by_teamled(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
    team_id: str = Path(...),
    memder_user_id: str = Query(...)
) -> None :
    result = await db_actions.add_user_to_team_byteamlead(team_id=team_id, user_id=user_id, membder_user_id=memder_user_id, db=db)
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    
@teams_router.patch("/{team_id}/", status_code=status.HTTP_202_ACCEPTED)
async def add_user_team(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
    team_id: str = Path(...)
) -> None:
    result = await db_actions.add_user_to_team(team_id=team_id, user_id=user_id, db=db)
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
