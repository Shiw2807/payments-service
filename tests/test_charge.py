"""
Tests for charge endpoint

WARNING: This test file contains FLAKY TESTS that depend on:
1. time.sleep() - makes tests slow and timing-dependent
2. Real network calls to httpbin.org - can fail due to network issues
"""
import pytest
import time
import requests
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.main import app

client = TestClient(app)


class TestChargeEndpoint:
    """Tests for the /api/payments/charge endpoint"""
    
    def test_create_charge_success(self):
        """Test successful charge creation"""
        response = client.post(
            "/api/payments/charge",
            json={
                "order_id": "order-123",
                "amount": 99.99,
                "currency": "USD",
                "customer_id": "cust-456",
                "payment_method": "card"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "succeeded"
        assert data["amount"] == 99.99
    
    def test_create_charge_invalid_amount(self):
        """Test charge with invalid amount"""
        response = client.post(
            "/api/payments/charge",
            json={
                "order_id": "order-123",
                "amount": -50,
                "currency": "USD",
                "customer_id": "cust-456",
                "payment_method": "card"
            }
        )
        assert response.status_code == 400
    
    def test_charge_missing_auth_vulnerability(self):
        """
        Test demonstrating the missing auth vulnerability.
        This test PASSES but highlights a security issue:
        The /charge endpoint accepts requests without any authorization.
        """
        # No authorization header provided - but request still succeeds!
        response = client.post(
            "/api/payments/charge",
            json={
                "order_id": "order-999",
                "amount": 1000.00,
                "currency": "USD",
                "customer_id": "victim-customer",
                "payment_method": "card"
            }
            # NOTE: No Authorization header!
        )
        # BUG: This should return 401, but returns 200
        # The endpoint lacks authorization check
        assert response.status_code == 200  # This is the vulnerability!


class TestFlakyTests:
    """
    FLAKY TESTS - These tests are intentionally unreliable
    They demonstrate common causes of test flakiness:
    1. Timing dependencies (time.sleep)
    2. External network dependencies (httpbin.org)
    """
    
    def test_flaky_with_sleep_and_network(self):
        """
        FLAKY TEST: Depends on time.sleep and real network call
        
        This test can fail due to:
        - Network latency variations
        - httpbin.org being slow or down
        - CI environment network restrictions
        - Rate limiting
        """
        # Artificial delay - makes test slow and timing-dependent
        time.sleep(1)
        
        # Real network call to external service - FLAKY!
        try:
            response = requests.get(
                "https://httpbin.org/delay/1",
                timeout=3  # Short timeout makes it more flaky
            )
            # This assertion can fail if httpbin is slow
            assert response.status_code == 200
        except requests.exceptions.Timeout:
            # Network timeout - test fails intermittently
            pytest.fail("Network request timed out - flaky test failure")
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection error - flaky test failure")
    
    def test_flaky_timing_dependent(self):
        """
        FLAKY TEST: Timing-dependent assertion
        
        This test checks if an operation completes within a time window,
        which can vary based on system load.
        """
        time.sleep(1)  # Unnecessary sleep
        
        start = time.time()
        
        # Make a charge request
        response = client.post(
            "/api/payments/charge",
            json={
                "order_id": "order-timing",
                "amount": 50.00,
                "currency": "USD",
                "customer_id": "cust-timing",
                "payment_method": "card"
            }
        )
        
        elapsed = time.time() - start
        
        # Flaky assertion - timing can vary
        # On slow CI machines, this might fail
        assert elapsed < 0.5, f"Request took too long: {elapsed}s"
        assert response.status_code == 200
    
    def test_flaky_external_api_dependency(self):
        """
        FLAKY TEST: Depends on external API availability
        
        Makes real HTTP request to httpbin.org which can:
        - Be temporarily unavailable
        - Have varying response times
        - Be blocked by firewalls
        """
        time.sleep(1)
        
        # External dependency - httpbin.org
        external_response = requests.get(
            "https://httpbin.org/json",
            timeout=5
        )
        
        # If httpbin is down, this fails
        assert external_response.status_code == 200
        
        # Use external data in our test
        external_data = external_response.json()
        assert "slideshow" in external_data


class TestRefundEndpoint:
    """Tests for the /api/payments/refund endpoint"""
    
    def test_refund_requires_auth(self):
        """Test that refund endpoint requires authorization"""
        response = client.post(
            "/api/payments/refund",
            json={
                "charge_id": "ch_123456",
                "amount": 50.00
            }
        )
        # Refund correctly requires auth (unlike /charge)
        assert response.status_code == 401
    
    def test_refund_with_auth(self):
        """Test refund with proper authorization"""
        # First create a charge
        charge_response = client.post(
            "/api/payments/charge",
            json={
                "order_id": "order-refund-test",
                "amount": 100.00,
                "currency": "USD",
                "customer_id": "cust-refund",
                "payment_method": "card"
            }
        )
        charge_id = charge_response.json()["id"]
        
        # Then refund with auth
        response = client.post(
            "/api/payments/refund",
            json={
                "charge_id": charge_id,
                "amount": 50.00,
                "reason": "Customer request"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
