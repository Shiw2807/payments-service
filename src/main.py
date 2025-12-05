"""
Payments Service - FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from .routes import payments, health
from .utils.validation import validate_order_total

app = FastAPI(
    title="Payments Service",
    description="Microservice for handling payments",
    version="1.0.0"
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])


@app.get("/")
async def root():
    return {
        "service": "payments-service",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3002))
    uvicorn.run(app, host="0.0.0.0", port=port)
