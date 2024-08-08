from sqlalchemy import Column, Integer, Boolean
from database.db_config import Base


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    tg_user_id = Column(Integer, unique=True)
    main_api_user_id = Column(Integer, unique=True)
    notice = Column(Boolean, default=False)
