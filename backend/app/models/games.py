from app.db.base import Base
from sqlalchemy import String,Integer,Column,Date,DateTime,Text
from datetime import datetime
from sqlalchemy.orm import relationship

class Game(Base):
    __tablename__="games"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    description=Column(Text)
    cover_image=Column(String)
    release_date=Column(Date)
    studio=Column(String)
    genre=Column(String,nullable=False)
    platform=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.now)
    rawg_id=Column(Integer)
    reviews=relationship(
        "Review",
        back_populates="game"
    )
