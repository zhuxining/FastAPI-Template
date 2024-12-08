from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import schemas
from app.api import deps
from app.models import Post, User

router = APIRouter()


@router.post("/", response_model=schemas.Post)
async def create_post(
    *,
    db: AsyncSession = Depends(deps.get_db),
    post_in: schemas.PostCreate,
    current_user: User = Depends(deps.get_current_active_user),
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


@router.get("/", response_model=List[schemas.Post])
async def read_posts(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
):
    result = await db.execute(
        select(Post).offset(skip).limit(limit)
    )
    posts = result.scalars().all()
    return posts


@router.get("/{post_id}", response_model=schemas.Post)
async def read_post(
    *,
    db: AsyncSession = Depends(deps.get_db),
    post_id: int,
    current_user: User = Depends(deps.get_current_active_user),
):
    result = await db.execute(select(Post).filter(Post.id == post_id))
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
    current_user: User = Depends(deps.get_current_active_user),
):
    result = await db.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if (post.author_id == current_user.id) is not True:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = post_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.delete("/{post_id}")
async def delete_post(
    *,
    db: AsyncSession = Depends(deps.get_db),
    post_id: int,
    current_user: User = Depends(deps.get_current_active_user),
):
    result = await db.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if (post.author_id == current_user.id) is not True:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await db.delete(post)
    await db.commit()
    return {"status": "success"}
