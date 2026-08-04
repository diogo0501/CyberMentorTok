from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.bookmark import Bookmark
from app.schemas.bookmark import BookmarkCreate, BookmarkResponse, BookmarkUpdate
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=list[BookmarkResponse])
async def list_bookmarks(
    folder: str | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = select(Bookmark).where(Bookmark.user_id == user.id)
    if folder:
        query = query.where(Bookmark.folder == folder)
    query = query.order_by(Bookmark.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=BookmarkResponse, status_code=201)
async def create_bookmark(
    data: BookmarkCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    bookmark = Bookmark(user_id=user.id, **data.model_dump())
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    return bookmark


@router.delete("/{bookmark_id}", status_code=204)
async def delete_bookmark(
    bookmark_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Bookmark).where(Bookmark.id == bookmark_id, Bookmark.user_id == user.id)
    )
    bookmark = result.scalar_one_or_none()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    await db.delete(bookmark)
    await db.commit()


@router.patch("/{bookmark_id}", response_model=BookmarkResponse)
async def update_bookmark(
    bookmark_id: str,
    data: BookmarkUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Bookmark).where(Bookmark.id == bookmark_id, Bookmark.user_id == user.id)
    )
    bookmark = result.scalar_one_or_none()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(bookmark, key, value)

    await db.commit()
    await db.refresh(bookmark)
    return bookmark
