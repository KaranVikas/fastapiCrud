from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Config

engine = AsyncEngine(
  create_engine(
  url=Config.DATABASE_URL,
  echo=True
  )
)
print("Engine created",engine)
print(Config.DATABASE_URL)

async def init_db():
  # creating an engine object 
  async with engine.begin() as conn:
    from src.books.models import Book

    await conn.run_sync(SQLModel.metadata.create_all)

async def get_session()->AsyncSession: # type: ignore
  Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
  )
    # class_=AsyncSession: Uses SQLModel’s async session class.
    # expire_on_commit=False: Prevents session expiration after commits (avoids reloading data unnecessarily).
  print("Before session created",Session)
  async with Session() as session:
    print("session created",session.bind)
    yield session

