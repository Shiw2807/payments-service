"""
Validation utilities for payments service

ISSUE: This is DUPLICATED LOGIC - the same validation exists in shared-utils
Both services implement their own version instead of using the shared library
"""


def validate_order_total(total: float) -> bool:
    """
    Validate an order total.
    
    This is duplicated from shared-utils/src/index.ts
    Should use shared-utils instead of maintaining duplicate code.
    
    Args:
        total: The order total to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Duplicated validation logic - should use shared-utils instead
    if not isinstance(total, (int, float)):
        return False
    if total != total:  # NaN check
        return False
    if total < 0:
        return False
    if total > 1000000:
        return False
    return True


def validate_currency(currency: str) -> bool:
    """
    Validate currency code.
    
    Args:
        currency: ISO 4217 currency code
        
    Returns:
        True if valid, False otherwise
    """
    valid_currencies = {"USD", "EUR", "GBP", "JPY", "CAD", "AUD"}
    return currency in valid_currencies


def validate_payment_method(method: str) -> bool:
    """
    Validate payment method.
    
    Args:
        method: Payment method identifier
        
    Returns:
        True if valid, False otherwise
    """
    valid_methods = {"card", "bank_transfer", "paypal", "apple_pay", "google_pay"}
    return method in valid_methods
