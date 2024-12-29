from typing import Annotated, List, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app import schemas
from app.api import deps
from app.models import Post, User

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=schemas.Post)
async def create_post(
    *,
    db: AsyncSession = Depends(deps.get_db),
    post_in: schemas.PostCreate,
    current_user: User = Depends(deps.current_active_user),
):
    post = Post(
        title=post_in.title,
        content=post_in.content,
        published=post_in.published,
        author_id=current_user.id,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"


@router.get("/", response_model=List[schemas.Post])
async def read_posts(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    filter_query: Annotated[FilterParams, Query()],
):
    result = await db.execute(select(Post).offset(filter_query.offset).limit(filter_query.limit))
    posts = result.scalars().all()
    return posts


@router.get("/{post_id}", response_model=schemas.Post)
async def read_post(
    *,
    db: AsyncSession = Depends(deps.get_db),
    post_id: int,
    current_user: User = Depends(deps.current_active_user),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(
    *,
    db: AsyncSession = Depends(deps.get_db),
    post_id: int,
    post_in: schemas.PostUpdate,
    current_user: User = Depends(deps.current_active_user),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    post_data = post_in.dict(exclude_unset=True)
    for key, value in post_data.items():
        setattr(post, key, value)

    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.delete("/{post_id}")
async def delete_post(
    *,
    db: AsyncSession = Depends(deps.get_db),
    post_id: int,
    current_user: User = Depends(deps.current_active_user),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await db.delete(post)
    await db.commit()
    return {"ok": True}
