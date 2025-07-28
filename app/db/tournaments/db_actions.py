from typing import List, Optional
from datetime import date
from enum import Enum


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.associative import UserTeamAssoc, Result, Role
from app.db.tournaments.models import Tournament
from app.db.teams.models import Team


class Vote(Enum):
    up_vote = 1
    down_vote = -1


async def create_tournament(name_tourna: str, db: AsyncSession, exp_days: int=7) -> None:
    tournament = Tournament(name_tourna=name_tourna, exp_days=exp_days)
    db.add(tournament)
    await db.commit()
    

async def join_tournament(user_id: str, team_id: str, tournament_id: str, db: AsyncSession) -> Optional[bool]:
    user_team_assoc: Optional[UserTeamAssoc] = await db.scalar(select(UserTeamAssoc).filter_by(user_id=user_id, team_id=team_id, role=Role.teamlead))
    tournament: Optional[Tournament] = await db.scalar(select(Tournament).filter(Tournament.id==tournament_id, Tournament.expire_date > date.today()))
    if not user_team_assoc or not tournament:
        return
    
    result = Result(team=user_team_assoc.team, tournament=tournament)
    db.add(result)
    await db.commit()
    return True


async def add_result_by_team(user_id: str, team_id: str, tournament_id: str, result: float, db: AsyncSession) -> Optional[bool]:
    user_team_assoc: Optional[UserTeamAssoc] = await db.scalar(select(UserTeamAssoc).filter_by(user_id=user_id, team_id=team_id, role=Role.teamlead))
    tournament: Optional[Tournament] = await db.scalar(select(Tournament).filter(Tournament.id==tournament_id, Tournament.expire_date < date.today()))
    if not user_team_assoc or not tournament:
        return
    
    tournament_result: Result = await db.scalar(select(Result).filter_by(tournament=tournament, team=user_team_assoc.team))
    tournament_result.result += result
    await db.commit()
    return True


async def add_vote(user_id: str, tournament_id: str, team_id: str, vote: Vote, db: AsyncSession) -> Optional[bool]:
    user_team_assoc: Optional[UserTeamAssoc] = await db.scalar(select(UserTeamAssoc).filter_by(user_id=user_id, team_id=team_id))
    result: Optional[Result] = await db.scalar(select(Result).filter_by(team=user_team_assoc.team, tournament_id=tournament_id))
    if not user_team_assoc or not result:
        return
    
    result.vote_result += vote.value
    await db.commit()
    return True


async def check_vote_result(user_id: str, tournament_id: str, team_id: str, db: AsyncSession) -> Optional[bool]:
    user_team_assoc: Optional[UserTeamAssoc] = await db.scalar(select(UserTeamAssoc).filter_by(user_id=user_id, team_id=team_id, role=Role.teamlead))
    result: Optional[Result] = await db.scalar(select(Result).filter_by(team=user_team_assoc.team, tournament_id=tournament_id))
    
    
    if result.vote_result < 0:
        result.tournament.teams.remove(user_team_assoc.team)
        await db.commit()
        return False
    return True


async def get_results(tournament_id: id, db: AsyncSession) -> List[Result]:
    return  await db.scalars(select(Result).filter_by(tournament_id=tournament_id))


async def get_tournament(db: AsyncSession):
    return await db.scalars(select(Tournament).filter(Tournament.expire_date > date.today()))