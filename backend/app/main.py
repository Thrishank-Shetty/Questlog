from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.models import *
from app.db.database import engine
from app.routes.game_route import router as game_router
from app.routes.review_route import router as review_router
from app.routes.user_route import router as user_router


app=FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=["http://localhost:3000"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(game_router)
app.include_router(review_router)
app.include_router(user_router)