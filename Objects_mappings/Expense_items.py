
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


class ExpenseItem(Base):
    __tablename__ = "expense_items"

    item_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    claim_id: Mapped[str] = mapped_column(
        ForeignKey("expense_claims.claim_id"),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    item_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    vendor: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    policy_limit: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    policy_flag: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    receipt_attached: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
