from sqlalchemy import ForeignKey, Integer, String, Text, Table, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(150), nullable=False)
    start_date = mapped_column(Date, nullable=False)

    employee: Mapped[list["Employee"]] = relationship(secondary="participations",back_populates="project", viewonly=True)

class Employee(Base):
    __tablename__ = "employees"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    email = mapped_column(String(120), nullable=False, unique=True)

    project: Mapped[list["Project"]] = relationship(secondary="participations", back_populates="employee", viewonly=True)

class Participation(Base):
    __tablename__ = "participations"

    project_id = mapped_column(Integer, ForeignKey("projects.id"), primary_key=True)
    employee_id = mapped_column(Integer, ForeignKey("employees.id"), primary_key=True)
    role = mapped_column(String(50), nullable=False)

