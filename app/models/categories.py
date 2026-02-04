from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)
    is_active = mapped_column(Boolean, default=True)
    parent_id = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)

    parent: Mapped["Category|None"] = relationship("Category", back_populates="children", remote_side="Category.id")

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")

    children: Mapped[list["Category"]] = relationship("Category", back_populates="parent")