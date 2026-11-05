
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Date,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from Objects_mappings.Employee import Base


class ExpenseClaim(Base):
    __tablename__ = "expense_claims"

    claim_id: Mapped[str] = mapped_column(
        String(20), primary_key=True
    )

    employee_id: Mapped[str] = mapped_column(
        ForeignKey("employees.employee_id"),
        nullable=False,
    )

    claim_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    trip_purpose: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    trip_city: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    trip_start: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    trip_end: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    approved_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    approval_level: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    approver_id: Mapped[str] = mapped_column(
        ForeignKey("employees.employee_id"),
        nullable=True,
    )

    payment_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )
    
    approval_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )

    exception_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )

    reason: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
