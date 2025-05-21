from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///ligadb.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Type(Base):
    __tablename__ = 'types'

    id:Mapped[int] = mapped_column(primary_key=True)
    name_type: Mapped[str] = mapped_column(String(255))

class Task(Base):
    __tablename__ = 'tasks'

    id:Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255))
    type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)