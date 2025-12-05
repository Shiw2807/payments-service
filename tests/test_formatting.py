"""
Tests for formatting utilities

This test file demonstrates the API contract change issue with shared-utils v2.0.0
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.formatting import format_currency_wrapper, format_payment_amount


class TestFormatCurrencyWrapper:
    """
    Tests demonstrating the API contract change issue.
    
    The shared-utils library changed formatCurrency signature in v2.0.0:
    - Old: formatCurrency(amount) 
    - New: formatCurrency(amount, locale)
    
    payments-service still uses the old signature, causing runtime failures.
    """
    
    def test_format_currency_fails_with_old_signature(self):
        """
        FAILING TEST: Demonstrates API contract change
        
        This test shows that calling formatCurrency with the old signature
        (without locale parameter) now fails in v2.0.0
        """
        with pytest.raises(RuntimeError) as exc_info:
            format_currency_wrapper(99.99)
        
        assert "locale parameter" in str(exc_info.value)
        assert "API Contract Change" in str(exc_info.value)
    
    def test_format_currency_expected_behavior(self):
        """
        This test documents what the expected behavior SHOULD be
        after fixing the API contract change.
        
        Currently fails because format_currency_wrapper uses old signature.
        """
        # This is what we WANT to happen after fixing:
        # result = format_currency_wrapper(99.99, 'en-US')
        # assert result == '$99.99'
        
        # But currently, even calling without locale raises an error
        with pytest.raises(RuntimeError):
            format_currency_wrapper(99.99)


class TestFormatPaymentAmount:
    """Tests for format_payment_amount function"""
    
    def test_format_usd(self):
        result = format_payment_amount(99.99, "USD")
        assert result == "$99.99"
    
    def test_format_eur(self):
        result = format_payment_amount(99.99, "EUR")
        assert result == "€99.99"
    
    def test_format_gbp(self):
        result = format_payment_amount(99.99, "GBP")
        assert result == "£99.99"
    
    def test_format_unknown_currency(self):
        result = format_payment_amount(99.99, "XYZ")
        assert result == "XYZ99.99"
    
    def test_format_default_currency(self):
        result = format_payment_amount(50.00)
        assert result == "$50.00"
