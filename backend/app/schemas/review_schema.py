from pydantic import BaseModel,ConfigDict,Field
from datetime import datetime

model_config=ConfigDict(from_attributes=True)

class ReviewCreate(BaseModel):
    rating:int = Field(ge=1,le=5)
    review_text:str | None=None

class ReviewResponse(BaseModel):
    rating:int
    review_text:str | None=None
    created_at:datetime

class ResponseReview(BaseModel):
    id:int
    rating:int
    review_text:str | None=None
    created_at:datetime