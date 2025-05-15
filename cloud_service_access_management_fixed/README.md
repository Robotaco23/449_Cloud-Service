# Cloud Service Access Management System

## Description
This FastAPI project implements a basic cloud service access management system with plans, permissions, subscriptions, and usage tracking.

## Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Directory Structure

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers
│       ├── plans.py
│       ├── permissions.py
│       ├── subscriptions.py
│       ├── usage.py
│       └── access_control.py
├── requirements.txt
└── README.md
```
