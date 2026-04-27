from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import models, engine, AsyncSessionLocal
from app.db.init_db import init_db
from app.api.routes.auth import router as auth_router
from app.api.routes.admins import router as admin_router
from app.api.routes.room import router as room_router
from app.api.routes.user import router as user_router
from app.api.routes.order import router as order_router
app = FastAPI()

# 1. 在启动时异步初始化数据库表结构
@app.on_event("startup")
async def startup_event():
    # 使用 engine.begin() 来创建表
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    
    # 2. 正确获取异步数据库会话并初始化数据
    async with AsyncSessionLocal() as db:
        await init_db(db)
        await db.commit()  # 确保初始化数据被提交

# 配置 CORS
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:4173",
    "http://localhost:4173",
    "http://localhost:5173",
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
app.include_router(user_router)
app.include_router(order_router)
