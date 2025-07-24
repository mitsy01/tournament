from typing import Optional, Annotated, List


from fastapi import APIRouter, status, HTTPException, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.tournaments import db_actions
from app.db.tournaments.models import Result
from app.pydantic_models.tournaments import TournamentModel, VoteModel, ResultModel, TournamentModelResponce
from app.routes.users import get_user_id
from app.db.base import get_db


tournaments_router = APIRouter(prefix="/tournaments", tags=["Tournament"])


@tournaments_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tournament(
    tournament_model: TournamentModel,
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends[get_db]],
):
    await db_actions.create_tournament(**tournament_model.model_dump(), db=db)


@tournaments_router.post("/join/", status_code=status.HTTP_202_ACCEPTED)
async def join_tournament(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[str, Depends(get_db)],
    team_id: str = Query(..., description="Team Id"),
    tournament_id: str = Query(..., description="Tournament Id")
):
    if not await db_actions.join_tournament(
        user_id=user_id,
        team_id=team_id,
        tournament_id=tournament_id,
        db=db
    ):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Неможливо доєднатися до змагання.")
    

@tournaments_router.patch("/", status_code=status.HTTP_200_OK)
async def add_result(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
    team_id: str = Query(...),
    tournament_id: str = Path(...),
    result: float = Query(...)
):
    if not await db_actions.add_result_by_team(
        user_id=user_id,
        team_id=team_id,
        tournament_id=tournament_id,
        result=result,
        db=db
    ):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    
@tournaments_router.patch("/{tournament_id}/", status_code=status.HTTP_202_ACCEPTED)
async def add_vote(
    vote_model: VoteModel,
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if not await db_actions.add_vote(
        **vote_model.model_dump(),
        user_id=user_id,
        db=db
    ):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    
@tournaments_router.get("/vote_result/", status_code=status.HTTP_200_OK)
async def check_vote_result(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
    team_id: str = Query(...),
    tournament_id: str = Query(...)
):
    result = await db_actions.check_vote_result(
        user_id=user_id,
        team_id=team_id,
        tournament_id=tournament_id,
        db=db
    )
    
    if result is None: 
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    if result:
        return dict(message="За результатами голосування гравців більшість вирішила взяти участь у турнірі.")
    else:
        return dict(message="За результатами голосування гравців більшість НЕ вирішила взяти участь у турнірі.")
    
    
@tournaments_router.get("/{tournament_id}/", status_code=status.HTTP_202_ACCEPTED, response_model=List[ResultModel])
async def get_results(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
    tournament_id: str = Path(...)
):
    results = await db_actions.get_results(tournament_id=tournament_id, db=db)
    results_model = []
    for result in results:
        results_model.append(ResultModel(
            team_name=result.team.name,
            tournament_name=result.tournament.name,
            result=result.result,
            vote_result=result.vote_result
        ))
    return results_model



@tournaments_router.get("/", status_code=status.HTTP_202_ACCEPTED, response_model=List[TournamentModelResponce])
async def get_tournaments(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await db_actions.get_tournament(db=db)