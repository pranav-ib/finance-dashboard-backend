from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY="supersecretkey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

security = HTTPBearer()

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pswd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pswd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expiry})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    


def get_current_user(token = Depends(security)):
    payload = verify_access_token(token.credentials)
    
    return payload