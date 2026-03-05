from sqlalchemy import Integer, Boolean, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = mapped_column(Integer, primary_key = True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    comment = mapped_column(Text)
    comment_date = mapped_column(DateTime, default=datetime.now)
    grade = mapped_column(Integer, nullable=False)
    is_active = mapped_column(Boolean, default=True)

    user : Mapped["User"] = relationship("User", back_populates="reviews")
    product: Mapped["Product"] = relationship("Product", back_populates="reviews")