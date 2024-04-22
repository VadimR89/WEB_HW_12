import cloudinary
import cloudinary.uploader
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Path,
    Query,
    UploadFile,
    File,
)
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserResponse
from src.services.auth import auth_service
from src.conf.config import config
from src.repository import users as repositories_users

router = APIRouter(prefix="/users", tags=["users"])
cloudinary.config(
    cloud_name=config.CLOUDINARY_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    secret_key=config.CLOUDINARY_SECRET_KEY,
    secure=True,
)


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
        """
The get_current_user function is a dependency that will be injected into the
    get_current_user endpoint. It uses the auth_service to retrieve the current user,
    and returns it if found.

:param user: User: Tell fastapi that the function expects a user object
:return: The user object that is stored in the database
:doc-author: Trelent
"""
    return user


@router.patch(
    "/avatar",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def get_current_user(
    file: UploadFile = File(),
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
        """
The get_current_user function is a dependency that will be used in the
    get_current_user endpoint. It takes an UploadFile object, which is a file
    uploaded by the user, and uses it to update their avatar URL. The function
    also takes a User object as well as an AsyncSession object from FastAPI's
    Depends() method.

:param file: UploadFile: Get the file from the request
:param user: User: Get the current user
:param db: AsyncSession: Create a database session
:param : Get the file from the request
:return: The current user
:doc-author: Trelent
"""
    public_id = f"Web/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    user = await repositories_users.update_avatar_url(user.email, res_url, db)
    return user
