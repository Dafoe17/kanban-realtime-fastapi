from fastapi import APIRouter, Depends, Form, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from src.api.dependencies import get_db, Session
from src.schemas import UserCreate
from src.services import AuthService
from src.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

# For OAuth2PasswordBearer
@router.post("/token-json")
async def token_json(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
    ):

    user = AuthService.login(db, form_data.username, form_data.password)
    access_token, _ = AuthService.create_tokens(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

# For cookies
@router.post("/login")
async def login(
    email: str,
    password: str,
    response: Response,
    db: Session = Depends(get_db)
    ):

    user = AuthService.login(db, email, password)
    access_token, refresh_token = AuthService.create_tokens(user.id)

    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        httponly=True, 
        secure=False,  # потом True верни
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/")
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False, # потом True верни
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/"
    )

    return {"message": "logged"}

@router.post("/sign-up")
async def sign_up(
    data: UserCreate,
    db: Session = Depends(get_db)
    ):
    AuthService.sign_up(db, data)
    return {"message": "signed_up"}

@router.post("/refresh")
async def refresh(
    response: Response,
    refresh_token: str = Cookie(None),
    ):
    
    new_access = AuthService.refresh(refresh_token)

    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,
        secure=False,  # потом True верни
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )

    return {"message": "refreshed"}

@router.patch("/logout")
async def logout(response: Response): 
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"message": "logged out"}
 