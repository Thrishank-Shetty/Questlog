from app.db.database import get_db
from fastapi import APIRouter,Depends ,HTTPException,Query
from app.schemas.game_schema import GameCreate,GameResponse,GameListResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.games import Game
from app.models.reviews import Review

router=APIRouter()

@router.post("/games",response_model=GameCreate)
def create_games(game:GameCreate,db:Session=Depends(get_db)):
    new_game=Game(
        title=game.title,
        description=game.description,
        genre=game.genre,
        platform=game.platform,
        release_date=game.release_date,
        studio=game.studio,
        cover_image=game.cover_image
        
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

@router.get("/games",response_model=list[GameListResponse])
def get_games(search: str | None=None,genre: str | None=None,platform: str | None=None,sort:str = Query("top_rated"),db:Session=Depends(get_db)):
    avg_rating=func.coalesce(func.avg(Review.rating),0).label("avg_rating")
    review_count=func.count(Review.id).label("review_count")
    query=(db.query(
        Game.id,
        Game.title,
        Game.cover_image,
        avg_rating,
        review_count
    )
    .outerjoin(Review,Review.game_id==Game.id)
    .group_by(Game.id)
    ) 
    if search is not None:
        query=query.filter(Game.title.ilike(f"%{search}%"))
    if genre is not None:
        query=query.filter(Game.genre.ilike(f"%{genre}%"))
    if platform is not None:
        query=query.filter(Game.platform.ilike(f"%{platform}%"))
    if sort == "top_rated":
        query=query.order_by(avg_rating.desc())
    elif sort == "most_rated":
        query=query.order_by(review_count.desc())
    elif sort == "new":
        query=query.order_by(Game.release_date.desc())
    return query.all()

@router.get("/games/{game_id}",response_model=GameResponse)
def get_game_by_id(game_id:int,db:Session=Depends(get_db)):
    avg_rating=func.coalesce(func.avg(Review.rating),0).label("avg_rating")
    review_count=func.count(Review.id).label("review_count")
    game_query=(db.query(
        Game.id,
        Game.title,
        Game.description,
        Game.genre,
        Game.platform,
        Game.release_date, 
        Game.studio,
        Game.cover_image,
        avg_rating,
        review_count
    )
    .filter(Game.id==game_id)
    .outerjoin(Review,Review.game_id==Game.id)
    .group_by(Game.id)
    
    )
    game=game_query.first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    review=db.query(Review).filter(Review.game_id==game_id).order_by(Review.created_at.desc()).all()
    reviews_list = [
        {
            "rating": r.rating,
            "review_text": r.review_text,
            "created_at": r.created_at
        }
        for r in review
    ]

    return {
        "id": game.id,
        "title": game.title,
        "description": game.description,
        "genre": game.genre,
        "platform": game.platform,
        "release_date": game.release_date,
        "studio": game.studio,
        "cover_image": game.cover_image,
        "avg_rating": game.avg_rating,
        "review_count": game.review_count,
        "reviews": reviews_list
    }
    
@router.put("/games/{game_id}",response_model=GameCreate)
def update_game(game_id:int,game:GameCreate,db:Session=Depends(get_db)):
    games=db.query(Game).filter(Game.id==game_id).first()
    if not games:
        raise HTTPException(status_code=404,detail="Game not found")
    else:
        games.title=game.title
        games.description=game.description
        games.genre=game.genre
        games.platform=game.platform
        games.release_date=game.release_date
        games.studio=game.studio
        games.cover_image=game.cover_image
        db.commit()
        db.refresh(games)
    return games

@router.delete("/games/{game_id}")
def delete_game(game_id,db:Session=Depends(get_db)):
    game=db.query(Game).filter(Game.id==game_id).first()
    if not game:
         raise HTTPException(status_code=404,detail="Game not found")
    db.delete(game)
    db.commit()
    return "Game deleted successfully"