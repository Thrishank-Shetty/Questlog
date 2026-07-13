from pydantic import BaseModel,ConfigDict
from datetime import date
from app.schemas.review_schema import ReviewResponse

model_config=ConfigDict(from_attributes=True)


class GameCreate(BaseModel):
    title:str
    description:str | None = None
    genre:str
    platform:str
    release_date:date
    studio:str | None = None
    cover_image:str | None = None


class GameResponse(BaseModel):
    id:int
    title:str
    description:str | None = None
    genre:str
    platform:str
    release_date:date
    studio:str | None = None
    cover_image:str | None = None
    avg_rating:float 
    review_count:int
    reviews: list[ReviewResponse] = []

class GameListResponse(BaseModel):
    id:int
    title:str
    cover_image:str | None = None
    avg_rating:float 
    review_count:int