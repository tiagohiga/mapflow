from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import User
from dependencies import get_session, validate_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def generate_token(id_user, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration
    jwt_info = {"sub": str(id_user), "exp": expiration_date}
    encoded_jwt = jwt.encode(jwt_info, SECRET_KEY, ALGORITHM)
    token = f"{encoded_jwt}"
    return token

def authenticate_user(email, senha, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(senha, user.password):
        return False
    return user

@auth_router.post("/create_user")
async def create_user(user_schema: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    else:
        encrypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, encrypted_password, user_schema.user_type, user_schema.is_active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"Message" : f"Usuário cadastrado com sucesso: {user_schema.email}."}
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = generate_token(user.id)
        refresh_token = generate_token(user.id, token_duration=timedelta(days=7))
        return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_type": user.user_type,
                "token_type": "Bearer"
               }
    
@auth_router.post("/login-swagger")
async def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = generate_token(user.id)
        return {
                "access_token": access_token,
                "user_type": user.user_type,
                "token_type": "Bearer"
               }
    
@auth_router.get("/refresh")
async def get_refresh_token(user: User = Depends(validate_token)):
    access_token = generate_token(user.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
           }