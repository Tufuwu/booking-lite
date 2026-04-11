from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

import app.repository as repository
import app.db.models as models
from app.db.database import engine, SessionLocal
from app.dependencies import get_db
from app.api.routes.admin import auth 
# from routers import (
#     user_router,
#     room_router,
#     order_router,
#     token_router,
#     admin_router,
#     admin_me_router,
# )
# from app import crud, schemas  # 根据你的项目结构调整

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)