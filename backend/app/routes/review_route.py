from fastapi import Depends,APIRouter,HTTPException
from app.models.reviews import Review
from app.schemas.review_schema import ReviewCreate,ReviewResponse,ResponseReview
from app.db.database import get_db
from sqlalchemy.orm import Session

router=APIRouter()

@router.get("/reviews",response_model=list[ResponseReview])
def get_response(db:Session=Depends(get_db)):
    review=db.query(Review).all()
    if not review:
        return []
    return review

@router.get("/games/{game_id}/reviews",response_model=list[ReviewResponse])
def get_response_id(game_id:int,db:Session=Depends(get_db)):
    review=db.query(Review).filter(Review.game_id==game_id).all()
    if not review:
        return []
    return review

@router.post("/games/{game_id}/review",response_model=ReviewResponse)
def create_review(game_id:int,review:ReviewCreate,db:Session=Depends(get_db)):
    new_review=Review(
        rating=review.rating,
        review_text=review.review_text,
        game_id=game_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.put("/games/reviews/{game_id}",response_model=ReviewCreate)
def update_review(game_id:int,review:ReviewCreate,db:Session=Depends(get_db)):
    review_q=db.query(Review).filter(Review.id==game_id).first()
    if not review_q:
        raise HTTPException(status_code=404, detail="Review not found")
    review_q.rating=review.rating
    review_q.review_text=review.review_text
    db.commit()
    db.refresh(review_q)
    return review_q

@router.delete("/games/reviews/{review_id}")
def delete_review(review_id:int,db:Session=Depends(get_db)):
    review_q=db.query(Review).filter(Review.id==review_id).first()
    db.delete(review_q)
    db.commit()
    return "Review deleted successfully"