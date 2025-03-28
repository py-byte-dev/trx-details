# trx-details

**`trx-details`** is a FastAPI-based microservice that allows you to quickly retrieve information about a TRON wallet — including TRX
balance, Bandwidth, and Energy.

This project was built as a test assignment, following the principles of **clean architecture and SOLID** for company Forkitech.

---

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL + SQLAlchemy
- tronpy
- Pytest
- Docker + Docker Compose

---

## Project Setup

1. **Create a configuration file based on the template:**
   ```bash
   cp .env.dist .env
   ```

2. **Edit the `.env` file and set the required environment variables:**
   ```env
   # Database configuration
   POSTGRES_USER=youruser
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_DB=yourdatabase

   # TRON API settings
   TRON_API_KEY=your_tron_api_key
   ```

3. **Start the services using Docker Compose:**
   ```bash
   docker-compose up -d
   docker exec -it db bash -c alembic upgrade head
   ```

---

## Examples of requests

### Get information about the wallet (by address)

```bash
curl -X POST "http://localhost:8000/api/wallet" \
  -H "Content-Type: application/json" \
  -d '{"address": "TLxMgDJhiHHQMs6NJrk5THWpdjDEuFQdqw"}'
```

**Example of a response:**

```json
{
  "address": "TLxMgDJhiHHQMs6NJrk5THWpdjDEuFQdqw",
  "balance": 123.456,
  "bandwidth": 5000,
  "energy": 10000
}
```

---

### Get a list of all requested wallets

```bash
curl -X GET "http://localhost:8000/api/event?page=1&page_size=2" -H "accept: application/json"
```

**Example of a response:**

```json
{
  "total": 2,
  "size": 2,
  "events": [
    {
      "id": "104832d1-b7b2-4eca-ad4c-b5df407d119d",
      "address": "TLxMgDJhiHHQMs6NJrk5THWpdjDEuFQdqw",
      "created_at": "2025-03-27T12:34:56"
    },
    {
      "id": "104832d1-b7b2-4eca-ad4c-b5df407d11921",
      "address": "TLxMgDJhiHHQMs6NJrk5THWpdjDEuFQdqw",
      "created_at": "2025-03-27T12:36:10"
    }
  ]
}

```

---

## Tests

1. **Create test database**

```bash
docker exec -it db psql -U postgres -c "CREATE DATABASE test;"
```

2. **Load Environment Variables**

```bash
export $(grep -v '^#' .env | xargs)
```

3. **Run Tests**

```bash
TEST_DB=test python3 -m pytest tests --asyncio-mode=auto
```

## API Documentation

Once the server is running, Swagger UI will be available at:  
[http://localhost:8000/api/docs](http://localhost:8000/api/docs)

