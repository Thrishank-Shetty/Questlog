from app.db.base import Base
from sqlalchemy import Text,Integer,Column,DateTime,ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__="reviews"
    id=Column(Integer,primary_key=True,index=True)
    rating=Column(Integer)
    review_text=Column(Text,nullable=True)
    created_at=Column(DateTime,default=datetime.now)
    game_id=Column(Integer,ForeignKey("games.id"))

    game=relationship(
        "Game",
        back_populates="reviews"
    )