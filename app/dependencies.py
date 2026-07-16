from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
from app.security import decode_access_token
from app.crud import view_user
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

def get_db():
    with SessionLocal() as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)      ) -> User:
                                            
    payload = decode_access_token(token=token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user")
    
    user = view_user(int(user_id), session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user")
    
    return user