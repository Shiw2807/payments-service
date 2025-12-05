"""
Payment routes
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import os

from ..services.payment_processor import PaymentProcessor
from ..utils.validation import validate_order_total

router = APIRouter()
payment_processor = PaymentProcessor()


class ChargeRequest(BaseModel):
    order_id: str
    amount: float
    currency: str = "USD"
    customer_id: str
    payment_method: str


class RefundRequest(BaseModel):
    charge_id: str
    amount: Optional[float] = None
    reason: Optional[str] = None


@router.post("/charge")
async def create_charge(request: ChargeRequest):
    """
    Create a new charge for an order.
    
    AUTH MISSING: This endpoint lacks authorization check!
    Any request can charge any customer without verification.
    Should check: authorization header, customer ownership, rate limiting
    """
    # BUG: No authorization check before processing payment!
    # Should verify:
    # 1. Valid API key or JWT token
    # 2. Customer owns this order
    # 3. Request is not a replay attack
    
    # Validate order total using local validation (DUPLICATED LOGIC)
    if not validate_order_total(request.amount):
        raise HTTPException(status_code=400, detail="Invalid amount")
    
    # Process payment without any auth verification
    result = await payment_processor.charge(
        order_id=request.order_id,
        amount=request.amount,
        currency=request.currency,
        customer_id=request.customer_id,
        payment_method=request.payment_method
    )
    
    return result


@router.post("/refund")
async def create_refund(
    request: RefundRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Create a refund for a charge.
    This endpoint HAS authorization (for comparison with /charge)
    """
    # This endpoint correctly checks authorization
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    result = await payment_processor.refund(
        charge_id=request.charge_id,
        amount=request.amount,
        reason=request.reason
    )
    
    return result


@router.get("/charges/{charge_id}")
async def get_charge(charge_id: str):
    """Get charge details by ID"""
    charge = await payment_processor.get_charge(charge_id)
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    return charge


@router.get("/orders/{order_id}/charges")
async def get_order_charges(order_id: str):
    """Get all charges for an order"""
    charges = await payment_processor.get_charges_by_order(order_id)
    return {"order_id": order_id, "charges": charges}
