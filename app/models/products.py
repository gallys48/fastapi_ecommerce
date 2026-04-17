from sqlalchemy import ForeignKey, String, Boolean, Integer, Numeric, Float, Computed, Index
from sqlalchemy.dialects.postgresql import TSVECTOR
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
    seller_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    rating = mapped_column(Float, default=0.0)

    tsv: Mapped[TSVECTOR] = mapped_column(
        TSVECTOR,
        Computed(
            """
            setweight(to_tsvector('english', coalesce(name, '')), 'A')
            || 
            setweight(to_tsvector('english', coalesce(description, '')), 'B')
            """,
            persisted=True,
        ),
        nullable=False,
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    seller: Mapped["User"] = relationship("User", back_populates="products")
    reviews: Mapped["Review"] = relationship("Review", back_populates="product")
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product")

    __table_args__ = (
        Index("ix_products_tsv", "tsv", postgresql_using="gin"),
    )
