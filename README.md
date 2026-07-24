# 🥛 Country Delight Clone API

A production-inspired backend clone of the Country Delight application built using **FastAPI**, **SQLAlchemy**, and **MySQL**. This project demonstrates authentication, product management, cart, orders, subscriptions, relationships, middleware, and exception handling.

---

## 🚀 Tech Stack

- FastAPI
- Python
- SQLAlchemy ORM
- MySQL
- JWT Authentication
- Passlib (bcrypt)
- Pydantic
- Python-Jose
- Uvicorn
  

---

## 📂 Project Structure

```
country-delight/

├── config/
│   └── settings.py
│
├── database/
│   └── database.py
│
├── models/
│   ├── user.py
│   ├── product.py
│   ├── address.py
│   ├── cart.py
│   ├── order.py
│   └── subscription.py
│
├── routes/
│   ├── auth.py
│   ├── product.py
│   ├── address.py
│   ├── cart.py
│   ├── order.py
│   └── subscription.py
│
├── schemas/
│   ├── user.py
│   ├── product.py
│   ├── address.py
│   ├── cart.py
│   ├── order.py
│   └── subscription.py
│
├── utils/
│   ├── hashing.py
│   ├── jwt.py
│   └── current_user.py
│
├── middleware/
│   └── logging.py
│
├── exceptions/
│   └── handlers.py
│
├── .env
├── main.py
├── requirements.txt
└── README.md
```

# 🗄 Database Schema

```
User
│
├── Address
├── Cart
│      └── CartItem
├── Orders
│      └── OrderItem
└── Subscription

Product
│
├── CartItem
├── OrderItem
└── Subscription
```

---

# ✨ Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Protected Routes
- Password Hashing

---

## Product Management

- Add Product
- Get All Products
- Get Product By Id
- Update Product
- Delete Product

---

## Address Management

- Add Address
- View User Addresses
- One User → Multiple Addresses

---

## Cart System

- Add Product to Cart
- View Cart
- Calculate Cart Total

---

## Order System

- Place Order
- Order History
- View Order Details
- Automatic Stock Reduction
- Cart Clear After Order

---

## Subscription System

- Create Subscription
- View Subscription
- Pause Subscription
- Resume Subscription
- Cancel Subscription

---

## Other Features

- SQLAlchemy Relationships
- Foreign Keys
- Dependency Injection
- Middleware
- Rate Limiting
- Global Exception Handling
- Environment Variables
- Lifespan Events

---


# 🔑 Authentication

The project uses JWT Authentication.

Protected APIs require:

```
Authorization: Bearer <access_token>
```

---

# 📌 API Endpoints

## Authentication

| Method | Endpoint |
|----------|----------------|
| POST | /auth/register |
| POST | /auth/login |

---

## Products

| Method | Endpoint |
|----------|----------------|
| POST | /products |
| GET | /products |
| GET | /products/{id} |
| PUT | /products/{id} |
| DELETE | /products/{id} |

---

## Address

| Method | Endpoint |
|----------|----------------|
| POST | /address |
| GET | /address |

---

## Cart

| Method | Endpoint |
|----------|----------------|
| POST | /cart/add |
| GET | /cart |

---

## Orders

| Method | Endpoint |
|----------|----------------|
| POST | /orders |
| GET | /orders |
| GET | /orders/{id} |

---

## Subscription

| Method | Endpoint |
|----------|----------------|
| POST | /subscriptions |
| GET | /subscriptions |
| PUT | /subscriptions/pause/{id} |
| PUT | /subscriptions/resume/{id} |
| DELETE | /subscriptions/{id} |


# Author

**Harsh Chauhan**

GitHub: https://github.com/Harsh-Chauhan108

LinkedIn: https://www.linkedin.com/in/harsh-chauhan-21bb49392/

---
