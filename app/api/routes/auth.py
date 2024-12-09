from fastapi import APIRouter

from app.api.deps import auth_backend, fastapi_users
from app.schemas import UserCreate, UserRead

router = APIRouter()

# Authentication routes
router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/jwt", tags=["auth"])

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    tags=["auth"],
)
