from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from models.agent import Agent
from schemas.agent import AgentCreate
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_current_agent(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Agent:
    # Logic to decode the token and retrieve the agent from the database
    # This is a placeholder for actual implementation
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def create_access_token(data: dict) -> str:
    # Logic to create a JWT token
    # This is a placeholder for actual implementation
    return "token"  # Replace with actual token generation logic