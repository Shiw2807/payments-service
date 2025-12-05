"""
Tests for validation utilities
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.validation import (
    validate_order_total,
    validate_currency,
    validate_payment_method
)


class TestValidateOrderTotal:
    """Tests for validate_order_total function"""
    
    def test_valid_positive_numbers(self):
        assert validate_order_total(100) is True
        assert validate_order_total(0) is True
        assert validate_order_total(999999) is True
        assert validate_order_total(0.01) is True
    
    def test_invalid_negative_numbers(self):
        assert validate_order_total(-1) is False
        assert validate_order_total(-100) is False
    
    def test_invalid_exceeds_max(self):
        assert validate_order_total(1000001) is False
        assert validate_order_total(10000000) is False
    
    def test_invalid_nan(self):
        assert validate_order_total(float('nan')) is False
    
    def test_invalid_non_numbers(self):
        assert validate_order_total("100") is False
        assert validate_order_total(None) is False


class TestValidateCurrency:
    """Tests for validate_currency function"""
    
    def test_valid_currencies(self):
        assert validate_currency("USD") is True
        assert validate_currency("EUR") is True
        assert validate_currency("GBP") is True
    
    def test_invalid_currencies(self):
        assert validate_currency("INVALID") is False
        assert validate_currency("usd") is False  # Case sensitive
        assert validate_currency("") is False


class TestValidatePaymentMethod:
    """Tests for validate_payment_method function"""
    
    def test_valid_methods(self):
        assert validate_payment_method("card") is True
        assert validate_payment_method("paypal") is True
        assert validate_payment_method("apple_pay") is True
    
    def test_invalid_methods(self):
        assert validate_payment_method("cash") is False
        assert validate_payment_method("bitcoin") is False
