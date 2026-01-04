from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    language_code: Mapped[str] = mapped_column(String(8), nullable=True)
    qr_token: Mapped[str] = mapped_column(String(255), nullable=True)


class Bussines(Base):
    __tablename__ = "bussines" 
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    address: Mapped[str] = mapped_column(String(255))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column()

class Staff(Base):
    __tablename__ = "staff"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    business_id: Mapped[int] = mapped_column(ForeignKey("bussines.id"))
    role: Mapped[str] = mapped_column(String(16))


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    business_id: Mapped[int] = mapped_column(ForeignKey("bussines.id"))
    required_stamps: Mapped[int] = mapped_column()
    reward: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)


class Card(Base):
    __tablename__ = "user_cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id"))
    current_stamps: Mapped[int] = mapped_column()
    status: Mapped[bool] = mapped_column(default=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)