from typing import Optional, List


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.associative import UserTeamAssoc, Result, Role
from app.db.teams.models import Team
from app.pydantic_models.teams import TeamModel
from app.db.users.models import User
from app.db.users.db_actions import get_user


async def create_team(user_id: str, team_model: TeamModel, db: AsyncSession):
    team = Team(**team_model.model_dump())
    user_team_accos = UserTeamAssoc(user_id=user_id, team=team, role=Role.teamlead)
    db.add(user_team_accos)
    await db.commit()
    

async def get_team(team_id: str, db: AsyncSession) -> Optional[Team]:
    return await db.scalar(select(Team).filter_by(id=team_id))


async def get_teams(private: Optional[bool], db: AsyncSession) -> List[Team]:
    if private is None:
        return await db.scalars(select(Team))
    else: 
        return await db.scalars(select(Team).filter_by(private=private))
    

async def del_team(team_id: str, user_id: str, db: AsyncSession) -> bool:
    user_team_assoc = await db.scalar(select(UserTeamAssoc).filter_by(user_id=user_id, team_id=team_id, role=Role.teamlead))
    if not user_team_assoc:
        return False
    
    await db.delete(user_team_assoc.team)
    await db.commit()
    return True


async def add_user_to_team_byteamlead(team_id: str, user_id: str, membder_user_id: str, db: AsyncSession): 
    user_team_assoc: Optional[Team] = await db.scalar(select(UserTeamAssoc).filter_by(user_id=user_id, team_id=team_id, role=Role.teamlead))
    user: Optional[User] = await get_user(user_id=membder_user_id, db=db)
    if not user_team_assoc or not user:
        return False
    
    user_team_assoc.users.append(user)
    await db.commit()
    return False


async def add_user_to_team(team_id: str, user_id: str, db: AsyncSession) -> bool:
    team: Optional[Team] = await db.scalar(select(UserTeamAssoc).filter_by(id==team_id, private=False))
    if not team:
        return False
    
    user: User = await get_user(user_id=user_id, db=db)
    team.users.append(user)
    await db.commit()
    return True