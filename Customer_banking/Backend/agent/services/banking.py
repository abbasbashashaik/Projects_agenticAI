
import re
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User
from models.customers import Customer
from models.Accounts import Account
from models.cards import Card
from models.transaction import Transaction


class NotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass


def get_customer_for_user(
    db: Session,
    user_id: int,
) -> Customer:
    stmt = (
        select(Customer)
        .join(User, Customer.user_id == User.id)
        .where(User.id == user_id)
    )

    customer = db.scalar(stmt)

    if customer is None:
        raise NotFoundError("Customer profile not found.")

    return customer


# 1. PROFILE DETAILS
def get_profile(db: Session, user_id: int) -> dict:
    customer = get_customer_for_user(db, user_id)

    return {
        "customer_id": customer.customer_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone_number": customer.phone_number,
        "kyc_status": customer.kyc_status,
    }


# 2. CONTACT UPDATE
def validate_contact(field: str, value: str) -> str:
    value = value.strip()

    if not value:
        raise ValidationError("Value cannot be empty.")

    if field == "email":
        if len(value) > 100:
            raise ValidationError("Email is too long.")

        if not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            value,
        ):
            raise ValidationError("Invalid email format.")

    elif field == "phone_number":
        # Example international-format validation.
        if not re.fullmatch(r"\+?[0-9 ()-]{7,20}", value):
            raise ValidationError("Invalid phone number.")

    else:
        raise ValidationError("Field is not editable.")

    return value


def update_contact(
    db: Session,
    user_id: int,
    field: str,
    value: str,
) -> dict:
    # Call this only AFTER explicit approval.
    value = validate_contact(field, value)
    customer = get_customer_for_user(db, user_id)

    setattr(customer, field, value)

    try:
        db.commit()
        db.refresh(customer)
    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "updated_field": field,
        "updated_value": value,
    }


# 3. MASKED CARD DETAILS
def mask_card_number(card_number: str) -> str:
    digits = "".join(
        char for char in card_number if char.isdigit()
    )

    # Do not expose malformed or unexpectedly short values.
    if len(digits) < 12 or len(digits) > 19:
        return "****"

    return "*" * (len(digits) - 4) + digits[-4:]


def get_cards(db: Session, user_id: int) -> list[dict]:
    stmt = (
        select(Card)
        .join(
            Account,
            Card.account_id == Account.account_id,
        )
        .join(
            Customer,
            Account.customer_id == Customer.customer_id,
        )
        .where(Customer.user_id == user_id)
    )

    cards = db.scalars(stmt).all()

    return [
        {
            "card_id": card.card_id,
            "card_number": mask_card_number(card.card_number),
            "card_type": card.card_type,
            "expiry_date": (
                card.expiry_date.isoformat()
                if card.expiry_date else None
            ),
            "status": card.status,
        }
        for card in cards
    ]


# 4. BALANCE
def get_balances(db: Session, user_id: int) -> list[dict]:
    stmt = (
        select(Account)
        .join(
            Customer,
            Account.customer_id == Customer.customer_id,
        )
        .where(Customer.user_id == user_id)
    )

    accounts = db.scalars(stmt).all()

    return [
        {
            "account_id": account.account_id,
            "account_type": account.account_type,
            "balance": str(account.balance),
            "status": account.status,
        }
        for account in accounts
    ]


# 5. TRANSACTION HISTORY
def get_transactions(
    db: Session,
    user_id: int,
    account_id: str | None = None,
    limit: int = 10,
) -> list[dict]:
    if not 1 <= limit <= 50:
        raise ValidationError("Limit must be between 1 and 50.")

    stmt = (
        select(Transaction)
        .join(
            Account,
            Transaction.account_id == Account.account_id,
        )
        .join(
            Customer,
            Account.customer_id == Customer.customer_id,
        )
        .where(Customer.user_id == user_id)
    )

    if account_id is not None:
        # This filter is applied in addition to ownership.
        stmt = stmt.where(Account.account_id == account_id)

    stmt = (
        stmt.order_by(Transaction.transaction_date.desc())
        .limit(limit)
    )

    transactions = db.scalars(stmt).all()

    return [
        {
            "transaction_id": tx.transaction_id,
            "account_id": tx.account_id,
            "amount": str(tx.amount),
            "transaction_type": tx.transaction_type,
            "description": tx.description,
            "transaction_date": (
                tx.transaction_date.isoformat()
                if tx.transaction_date else None
            ),
        }
        for tx in transactions
    ]


def propose_contact_update(
    db: Session,
    user_id: int,
    field: str,
    value: str,
) -> dict:
    value = validate_contact(field, value)
    customer = get_customer_for_user(db, user_id)

    current_value = getattr(customer, field)

    if current_value == value:
        return {"message": "No change required."}

    return {
        "requires_approval": True,
        "field": field,
        "current_value": current_value,
        "proposed_value": value,
        "message": (
            f"Confirm changing {field} from "
            f"{current_value} to {value}."
        ),
    }