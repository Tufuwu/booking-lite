from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.repository import admins
from app.db import models
from app.db import engine, SessionLocal
from app import core
from app.api.routes.admin.auth import router as auth_router
from app.api.routes.admin.admins import router as admin_router
from app.api.routes.admin.room import router as room_router 
from app.db import redis_client
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
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()

    try:
        existing = await admins.get_all_admins(db)
        if existing:
            return

        hashed_password = core.security.hash_password("admin123")

        admin = models.Admin(
            job_number="0001",
            name="Super Admin",
            hashed_password=hashed_password
        )

        await admins.create_admin(db, admin)

    finally:
        db.close()


origins = [
    "http://localhost:8080",
    "http://127.0.0.1:4173",
    "http://localhost:4173",
    "null",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(room_router)
