
from datetime import date

from sqlalchemy import Date, ForeignKey,ForeignKeyConstraint, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employees"

    employee_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    grade: Mapped[str | None] = mapped_column(String(20), nullable=True)
    grade_title: Mapped[str | None] = mapped_column(String(100), nullable=True)
    home_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    join_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    cost_center: Mapped[str | None] = mapped_column(String(50), nullable=True)
    manager_id: Mapped[str | None] = mapped_column(nullable=True)
