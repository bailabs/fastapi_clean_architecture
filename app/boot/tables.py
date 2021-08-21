from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
from app.boot.engine import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    identifier = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    salt = Column(String(500))
    key = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    user_info = relationship("UserInfo", back_populates="user")
    __table_args__ = tuple(
        UniqueConstraint("id", "identifier", "email", name="users_uc")
    )


class UserInfo(Base):
    __tablename__ = "userinfo"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fullname = Column(String, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_info")


class BlackListedAuthToken(Base):
    __tablename__ = "blacklisted_token"

    auth_token = Column(String, primary_key=True, index=True)


Base.metadata.create_all(bind=engine)
