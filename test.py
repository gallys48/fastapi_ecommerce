from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db
from sqlalchemy import select, update
from app.models.promocode import PromoCodeModel

router = APIRouter()

@router.delete("/{promocode_id}", status_code=status.HTTP_200_OK)
async def delete_promocode(promocode_id:int, db:AsyncSession = Depends(get_async_db)):
    promocode_smth = await db.scalars(select(PromoCodeModel).where(PromoCodeModel.id == promocode_id,
                                                             PromoCodeModel.is_active == True))
    db_promocode = promocode_smth.first()
    if db_promocode is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="promocode not found")

    await db.execute(update(PromoCodeModel).where(PromoCodeModel.id == promocode_id).values(is_active = False))
    await db.commit()
    return {"status": "success", "message": "Promocode marked as inactive"}







