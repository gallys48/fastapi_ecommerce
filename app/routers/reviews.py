from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.models.categories import Category as CategoryModel
from app.models.users import User as UserModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.schemas import Review as ReviewSchema, ReviewCreate
from app.db_depends import get_db, get_async_db
from app.auth import get_current_buyer, get_current_admin, get_current_user

router = APIRouter(
    tags=["reviews"]
)

@router.get("/reviews", response_model=list[ReviewSchema], status_code=status.HTTP_200_OK)
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))

    reviews = result.all()

    return reviews

@router.get("/products/{product_id}/reviews", response_model=list[ReviewSchema], status_code=status.HTTP_200_OK)
async def get_reviews_of_product(product_id:int, db:AsyncSession = Depends(get_async_db)):
    product_result = await db.scalars(select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True))
    product = product_result.first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or deleted")

    reviews_result = await db.scalars(select(ReviewModel).where(ReviewModel.product_id == product_id, ReviewModel.is_active == True))
    reviews = reviews_result.all()

    return reviews

@router.post("/reviews", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def add_review(review: ReviewCreate, db:AsyncSession = Depends(get_async_db), current_user = Depends(get_current_buyer)):
    product_result = await db.scalars(select(ProductModel).where(ProductModel.id == review.product_id, ProductModel.is_active == True))
    product = product_result.first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or deleted")

    if review.grade >5 or review.grade < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Grade must be in range 1-5")

    db_review = ReviewModel(
        user_id = current_user.id,
        product_id = review.product_id,
        comment = review.comment,
        grade = review.grade
    )

    db.add(db_review)
    await db.commit()
    await update_product_rating(db, review.product_id)

    return db_review

@router.delete("/reviews/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(review_id: int, db: AsyncSession = Depends(get_async_db), current_user = Depends(get_current_user)):
    review_result = await db.scalars(select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active == True))
    review = review_result.first()
    print(f"{current_user.id}-------------------------------")
    print(f"{review.user_id}-------------------------------")
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or deleted")

    if review.user_id != current_user.id:
        if current_user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin or author of review can perform this action")

    await db.execute(update(ReviewModel).where(ReviewModel.id == review.id).values(is_active = False))
    await db.commit()
    await db.refresh(review)
    await update_product_rating(db, review.product_id)

    return {"status": "success", "message": "Review marked as inactive"}

async def update_product_rating(db:AsyncSession, product_id: int):
    result = await db.scalars(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.first() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()