from uuid import uuid4
from typing import List
from datetime import date, timedelta, datetime, timezone


from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.db.base import Base
from app.db.associative import TeamTournamentAssoc


class Tournament(Base):
    __tablename__ = "tournaments"
    
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name_tourna: Mapped[str] = mapped_column(String(100))
    expire_date: Mapped[date] = mapped_column(Date())
    teams: Mapped[List["Team"]] = relationship(secondary=TeamTournamentAssoc.__tablename__, back_populates="touranemnts", lazy="selectin")
    
    def __init__(self, **kwargs):
        self.id = uuid4().hex
        self.expire_date = datetime.now(timezone.utc) + timedelta(days=7)
        super().__init__(**kwargs)