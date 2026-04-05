# Finance Data Processing & Access Control Backend

A backend service implementing RESTful APIs for managing financial records with **role-based access control, authentication, filtering, and analytics APIs**.


---

# Features

- JWT Authentication
- Role-Based Access Control (RBAC)
- Financial Record Management (CRUD)
- Flexible Record Filtering
- Search Support
- Dashboard Analytics
- User Management
- User Status Management (Active / Inactive)

---

# Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Backend framework |
| SQLite | Database |
| SQLAlchemy | ORM |
| Pydantic | Data validation |
| python-jose | JWT authentication |
| Passlib (bcrypt) | Password hashing |
| Uvicorn | ASGI server |

---

# Project Structure

```
app/
│
├── models/
│   ├── user.py
│   └── record.py
│
├── schemas/
│   ├── user_schema.py
│   └── record_schema.py
│
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── records.py
│   └── dashboard.py
│
├── database.py
├── security.py
└── main.py
```

---


# User Roles

The system implements **Role-Based Access Control (RBAC)**.

| Role | Permissions |
|---|---|
| Viewer | View their own records and dashboard |
| Analyst | View all records and analytics |
| Admin | Full control over records and users |

---

# Authentication Flow

```
User registers
      ↓
Password hashed using bcrypt
      ↓
User logs in
      ↓
JWT token generated
      ↓
Token used to access protected endpoints
```

Inactive users are blocked from both **login and API access**.

---

# Financial Records

Each record contains:

| Field | Description |
|---|---|
| amount | Transaction value |
| type | income or expense |
| category | Transaction category |
| date | Date of transaction |
| note | Optional description |
| created_by | User ID |
| created_at | Timestamp |

Validation ensures:

- Amount must be **positive**
- Type must be **income or expense**
- Category cannot be empty

---

# Record Filtering

The records endpoint supports flexible filtering.

### Endpoint

```
GET /records
```

### Query Parameters

| Parameter | Description |
|---|---|
| type | income / expense |
| category | filter by category |
| start_date | filter records after date |
| end_date | filter records before date |
| search | search in category or note |

Example:

```
GET /records?type=expense&category=food&start_date=2024-01-01
```

---

# Dashboard Analytics

Analytics endpoints provide financial insights.

| Endpoint | Description |
|---|---|
| /dashboard/total-income | Total income |
| /dashboard/total-expense | Total expenses |
| /dashboard/net-balance | Net balance |
| /dashboard/category-summary | Spending per category |
| /dashboard/recent-records | Latest transactions |
| /dashboard/monthly-trends | Monthly income vs expense trends |

---

# User Management

Admins can manage users via API.

### Capabilities

- View all users
- Update user roles
- Activate or deactivate users

Inactive users cannot access protected APIs.

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```
http://localhost:8000/docs
```

---

# Installation

### 1. Clone the repository

```
git clone https://github.com/pranav-ib/finance-dashboard-backend.git
cd finance-dashboard-backend
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the server

```
uvicorn app.main:app --reload
```

### 4. Open API documentation

```
http://localhost:8000/docs
```

---
