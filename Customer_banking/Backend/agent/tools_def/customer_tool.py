from langchain_core.tools import tool
from agent.guardrails.masking import mask_value

@tool
def get_balance():
    """This tool is called to check the balance of the user query"""
    return "your balance is 200090"

@tool
def mask_banking_pii(
    account_number: str | None = None,
    card_number: str | None = None,
) -> dict:
    """Mask account and card numbers before displaying them to a user.
    Keep only the last four digits visible.
    """
    return {
        "account_number": mask_value(account_number),
        "card_number": mask_value(card_number)
    }