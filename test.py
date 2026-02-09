from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import select, update
from app.models.post import PostModel

router = APIRouter()

@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def get_users(post_id:int, db: Session = Depends(get_db)):
    post = db.scalars(select(PostModel).where(PostModel.id == post_id,
                                              PostModel.is_active == True)).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or inactive")

    db.execute(update(PostModel).where(PostModel.id == post_id).values(is_active = False))
    db.commit()
    return "Post marked as inactive"