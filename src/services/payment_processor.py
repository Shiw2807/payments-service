"""
Payment processor service
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, List


class PaymentProcessor:
    """
    Handles payment processing operations.
    In production, this would integrate with Stripe, PayPal, etc.
    """
    
    def __init__(self):
        # In-memory storage for demo
        self._charges: Dict[str, dict] = {}
        self._refunds: Dict[str, dict] = {}
    
    async def charge(
        self,
        order_id: str,
        amount: float,
        currency: str,
        customer_id: str,
        payment_method: str
    ) -> dict:
        """
        Process a payment charge.
        
        In production, this would:
        1. Validate payment method
        2. Call payment gateway API
        3. Handle 3D Secure if needed
        4. Store transaction record
        """
        charge_id = f"ch_{uuid.uuid4().hex[:16]}"
        
        charge = {
            "id": charge_id,
            "order_id": order_id,
            "amount": amount,
            "currency": currency,
            "customer_id": customer_id,
            "payment_method": payment_method,
            "status": "succeeded",
            "created_at": datetime.utcnow().isoformat(),
        }
        
        self._charges[charge_id] = charge
        return charge
    
    async def refund(
        self,
        charge_id: str,
        amount: Optional[float] = None,
        reason: Optional[str] = None
    ) -> dict:
        """Process a refund for a charge."""
        if charge_id not in self._charges:
            raise ValueError(f"Charge {charge_id} not found")
        
        original_charge = self._charges[charge_id]
        refund_amount = amount or original_charge["amount"]
        
        refund_id = f"re_{uuid.uuid4().hex[:16]}"
        refund = {
            "id": refund_id,
            "charge_id": charge_id,
            "amount": refund_amount,
            "reason": reason,
            "status": "succeeded",
            "created_at": datetime.utcnow().isoformat(),
        }
        
        self._refunds[refund_id] = refund
        return refund
    
    async def get_charge(self, charge_id: str) -> Optional[dict]:
        """Get a charge by ID."""
        return self._charges.get(charge_id)
    
    async def get_charges_by_order(self, order_id: str) -> List[dict]:
        """Get all charges for an order."""
        return [
            charge for charge in self._charges.values()
            if charge["order_id"] == order_id
        ]
