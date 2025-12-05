# payments-service

Payments microservice built with Python and FastAPI.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn src.main:app --reload --port 3002

# Or run directly
python -m src.main
```

## Port

The service runs on **port 3002** by default.

Set `PORT` environment variable to change:
```bash
PORT=3003 python -m src.main
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check |
| POST | `/api/payments/charge` | Create a charge |
| POST | `/api/payments/refund` | Create a refund |
| GET | `/api/payments/charges/{id}` | Get charge by ID |
| GET | `/api/payments/orders/{id}/charges` | Get charges for order |

## API Documentation

FastAPI provides automatic API documentation:
- Swagger UI: http://localhost:3002/docs
- ReDoc: http://localhost:3002/redoc

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 3002 |

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run excluding flaky tests
pytest tests/ -v -k "not flaky"

# Run with coverage
pytest tests/ -v --cov=src
```

## Known Issues

⚠️ **Missing Authorization**: The `POST /api/payments/charge` endpoint lacks authorization checks. See `tests/test_charge.py` for details.

⚠️ **API Contract Change**: The `shared-utils` library v2.0.0 changed the `formatCurrency` function signature. The `locale` parameter is now required. See `tests/test_formatting.py` for the failing test.

⚠️ **Flaky Tests**: Some tests in `tests/test_charge.py` are intentionally flaky due to `time.sleep()` and external network calls to `httpbin.org`.

## License

MIT
