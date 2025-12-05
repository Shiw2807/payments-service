"""
Formatting utilities for payments service

This module demonstrates the API contract change issue with shared-utils v2.0.0
"""

# Simulating import from shared-utils
# In real scenario, this would be: from shared_utils import format_currency
# For demo, we simulate the function call pattern


def format_currency_wrapper(amount: float) -> str:
    """
    Format currency using shared-utils.
    
    BUG: Using old formatCurrency signature - missing locale parameter
    This will fail at runtime with shared-utils v2.0.0
    
    The old signature was: formatCurrency(amount)
    The new signature is: formatCurrency(amount, locale)
    
    Args:
        amount: The amount to format
        
    Returns:
        Formatted currency string
    """
    # Simulating the call to shared-utils with OLD signature
    # In shared-utils v2.0.0, this would throw:
    # "locale parameter is required in v2.0.0"
    
    # This is what the code looks like - calling without locale
    # format_currency(amount)  # Missing locale parameter!
    
    # For demo purposes, we'll simulate the error
    raise RuntimeError(
        "API Contract Change: formatCurrency now requires locale parameter. "
        "Old: formatCurrency(amount) -> New: formatCurrency(amount, locale)"
    )


def format_payment_amount(amount: float, currency: str = "USD") -> str:
    """
    Format a payment amount for display.
    
    Args:
        amount: The amount to format
        currency: Currency code
        
    Returns:
        Formatted amount string
    """
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
    }
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol}{amount:.2f}"
