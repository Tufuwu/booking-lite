from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 注意：sqlite 异步驱动需要使用 aiosqlite
DATABASE_URL = "sqlite+aiosqlite:///./hotel_booking.db"

# 1. 创建异步引擎
engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)



