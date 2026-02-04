from sqlalchemy import ForeignKey, String, Boolean, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from decimal import Decimal


class Product(Base):
    __tablename__ = "products"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(String(500), nullable = True)
    price = mapped_column(Numeric(10,2), nullable=False)
    image_url = mapped_column(String(200), nullable= True)
    stock = mapped_column(Integer, nullable=False)
    is_active = mapped_column(Boolean, default=True)
    category_id = mapped_column(Integer, ForeignKey("categories.id"), nullable= False)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
