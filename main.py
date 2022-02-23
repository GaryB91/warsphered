from datetime import timedelta, datetime
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from sql.database import SessionLocal



# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# main app
app = FastAPI()

# db init connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    user = crud.get_user_by_email(db, email)
    return user \
        if user and verify_password(password, user.hashed_password) \
        else None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    encode_data = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    encode_data.update({"exp": expire})
    return jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # pass username as email
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



# User routes
# authed endpoint
@app.get("/users/me/", response_model=schemas.User)
def get_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

###


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user, get_password_hash)


@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Game routes
@app.post("/users/{user_id}/games/", response_model=schemas.Game)
def create_user_game(user_id:int, data: schemas.GameCreate, db: Session = Depends(get_db)):
    return crud.create_game(db, **data, creator_id=user_id)


@app.get("/users/{user_id}/games/", response_model=list[schemas.Game])
def get_games_by_creator(user_id: int, db: Session = Depends(get_db)):
    return crud.get_games_by_creator(db, creator_id=user_id)


@app.get("/games/{game_id}", response_model=schemas.Game)
def get_game(user_id: int, game_id: int, db: Session = Depends(get_db)):
    return crud.get_game(db, game_id=game_id)


@app.get("/games/", response_model=list[models.Game])
def get_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_games(db, skip=skip, limit=limit)


@app.post("/games/{game_id}/{user_id}", response_model=models.Player)
def add_player(game_id: int, user_id: int, data: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.create_player(db, **data, game_id=game_id, user_id=user_id)

@app.get("/games/{game_id}/players", response_model=list[schemas.Player])
def get_players_for_game(game_id: int, db: Session = Depends(get_db)):
    return crud.get_players_by_game(db, game_id)


@app.get("/")
async def root():
    return {"message": "Hello World!"}

