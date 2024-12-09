from fastapi import APIRouter, Depends

from app.api.deps import current_active_user, fastapi_users
from app.models.user import User
from app.schemas import UserRead, UserUpdate

router = APIRouter()

# User management routes
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["users"],
)


@router.get("/me", tags=["users"])
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!", "user": user}