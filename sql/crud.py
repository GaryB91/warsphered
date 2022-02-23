from sqlalchemy.orm import Session
from sql import models, schemas


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user:  schemas.UserCreate, hasher) -> models.User:
    hashed_password = hasher(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_game(db: Session, game_id: int) -> models.Game | None:
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def get_games(db: Session, skip: int = 0, limit: int = 100) -> list[models.Game]:
    return db.query(models.Game).offset(skip).limit(limit).all()


def get_games_by_creator(db: Session, creator_id: int) -> list[models.Game]:
    return db.query(models.Game).filter(models.Game.creator_id == creator_id).all()


def create_game(db: Session, data: schemas.GameCreate, creator_id: int) -> models.Game:
    db_game = models.Game(**data, creator_id=creator_id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_players_by_game(db: Session, game_id: int) -> list[models.Player]:
    return db.query(models.Player).filter(models.Player.game_id == game_id).all()


def create_player(db: Session, data: schemas.PlayerCreate, game_id: int, user_id: int) -> models.Player:
    db_player = models.Player(**data, game_id=game_id, user_id=user_id)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player
