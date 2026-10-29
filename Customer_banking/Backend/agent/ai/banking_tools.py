
import json

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from agent.services.banking import (
    get_profile,
    propose_contact_update,
    get_cards,
    get_balances,
    get_transactions,
    ValidationError,
    NotFoundError,
)


def build_banking_tools(
    db: Session,
    authenticated_user_id: int,
):
    # Bind identity from the trusted backend.
    # Do not add user_id to any tool's model-facing arguments.

    @tool
    def show_profile() -> str:
        """Show the logged-in customer's name, email,
        phone number and KYC status."""
        return json.dumps(
            get_profile(db, authenticated_user_id)
        )

    @tool
    def propose_contact_change(
        field: str,
        value: str,
    ) -> str:
        """Propose an email or phone update.
        Never apply a change without human approval."""
        try:
            result = propose_contact_update(
                db,
                authenticated_user_id,
                field,
                value,
            )
            return json.dumps(result)
        except (ValidationError, NotFoundError) as exc:
            return json.dumps({"error": str(exc)})

    @tool
    def show_my_cards() -> str:
        """Show the logged-in user's cards with
        masked card numbers only."""
        return json.dumps(
            get_cards(db, authenticated_user_id)
        )

    @tool
    def check_my_balances() -> str:
        """Show balances for the logged-in user's accounts."""
        return json.dumps(
            get_balances(db, authenticated_user_id)
        )

    @tool
    def show_my_transactions(
        account_id: str = "",
        limit: int = 10,
    ) -> str:
        """Show recent transactions for the logged-in user.
        An optional account ID narrows the results but
        never bypasses ownership filtering."""
        try:
            result = get_transactions(
                db,
                authenticated_user_id,
                account_id=account_id or None,
                limit=limit,
            )
            return json.dumps(result)
        except (ValidationError, NotFoundError) as exc:
            return json.dumps({"error": str(exc)})

    return [
        show_profile,
        propose_contact_change,
        show_my_cards,
        check_my_balances,
        show_my_transactions,
    ]
