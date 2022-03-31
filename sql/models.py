from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sql.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    games = relationship("Game", back_populates="creator")
    players = relationship("Player", back_populates="user")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, default="")
    creator_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="games")
    players = relationship("Player", back_populates="game")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    description = Column(String)

    user = relationship("User", back_populates="players")
    game = relationship("Game", back_populates="players")
