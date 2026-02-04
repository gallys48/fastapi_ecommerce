from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema, CategoryCreate
from app.db_depends import get_db

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/")
async def get_all_categories():
    """
    Возвращает список всех категорий товаров.
    """
    return {"message": "Список всех категорий"}

@router.post("/")
async def create_category():
    """
    Создаёт новую категорию.
    """
    return {"message": "Категория создана"}

@router.put("/{category_id}")
async def update_category(category_id:int):
    """
    Обновляет категорию по её ID.
    """
    return {"message": f"Категория с ID {category_id} создана"}

@router.delete("/{category_id}")
async def delete_category(category_id:int):
    """
    Удаляет категорию по её ID.
    """
    return {"message": f"Категория с ID {category_id} удалена"}
