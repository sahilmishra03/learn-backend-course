from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import models, schemas, utils, database
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI, HTTPException, Response, status, Depends,APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings
oauth2_scheme = HTTPBearer()

#SECREY_KEY
#Algorithm
#Expriation Time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # user_id may be encoded as an int; keep it as-is so TokenData can handle it
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(credentials.credentials, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    if user is None:
        raise credentials_exception
    return user