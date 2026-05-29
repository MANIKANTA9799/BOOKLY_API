from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserBookModel,UserLogin
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from datetime import date,datetime, timedelta
from src.auth.utils import create_access_token, decode_token,verify_password
from fastapi.responses import JSONResponse
from src.db.redis import add_jti_to_blocklist
from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,#type:ignore
)
#type:ignore
auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin"])
@auth_router.post(
    "/signup", response_model=UserBookModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user

@auth_router.get("/me",response_model=UserBookModel)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.post('/login')
async def login_users(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    passwd = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise HTTPException(
            status_code=403,
            detail="User not found"
        )

    is_valid = verify_password(
        passwd,
        user.password_hash
    )

    if not is_valid:
        raise HTTPException(
            status_code=403,
            detail="Invalid password"
        )

    access_token = create_access_token(
        user_data={
            'email': user.email,
            'user_uid': str(user.uid)
        },
        expiry=timedelta(seconds=3600),
        refresh=False
    )

    refresh_token = create_access_token(
        user_data={
            'email': user.email,
            'user_uid': str(user.uid)
        },
        expiry=timedelta(days=2),
        refresh=True
    )

    return JSONResponse(
        content={
            "message": "Login Successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "uid": str(user.uid)
            }
        }
    )


@auth_router.get('/refresh_token')
async def get_new_access_token(token_details : dict = Depends(RefreshTokenBearer())):
   expiry_timestamp = token_details['exp']
   if datetime.fromtimestamp(expiry_timestamp):
       new_access_token = create_access_token(
           user_data = token_details['user'],
            expiry=timedelta(seconds=3600),
        refresh=False
       )
       return JSONResponse(
           content={
               "access_token":new_access_token
           }
       )
   raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expied token"
    )


@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):

    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )