from sqlalchemy import Column, Integer, Boolean, String

from src.database.db_config import Base


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    tg_user_id = Column(Integer, unique=True)
    uwords_uid = Column(String, unique=True)
