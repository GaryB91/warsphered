from pydantic import BaseModel

class PlayerBase(BaseModel):
    description: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    user_id: int
    game_id: int

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    url: str


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    owner_id: int
    players: list[Player] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    players: list[Player] = []
    games: list[Game] = []


    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
