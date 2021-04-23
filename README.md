# api_auth

## Overview
The Authentication API of My Company.
Powered by [FastAPI](https://fastapi.tiangolo.com/) and SQL Alchemy.

## How to Install

Install required dependencies

```python3 -m pip install requirements/pkg.whl```

Run server through uvicorn

`uvicorn main:app --reload`
and wait for it to complete making the database users.db

Run alembic migration for any updates

`alembic upgrade head`

## Endpoints
  visit `http://localhost:8000/docs`
