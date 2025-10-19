# 🏪 Store API (Django + DRF)

A full-featured e-commerce REST API built with **Django REST Framework**, including authentication with **JWT**, product management, shopping cart, and order processing — all with consistent validation and custom error handling.

---

## 🚀 Features

- **JWT Authentication** (login, refresh, verify)
- **Admin-only CRUD** for Products and Categories
- **Shopping Cart** with item merge, stock validation, and quantity updates
- **Order system** with checkout, pay, and cancel endpoints
- **Custom validation errors** (consistent `detail`, `key`, `available`)
- **Pagination, filtering, and search**
- **Auto-generated API docs** (Swagger / Redoc via drf-spectacular)

---

## 🧩 Tech Stack

- Python 3.12  
- Django 5.x  
- Django REST Framework  
- drf-spectacular (OpenAPI / Swagger docs)  
- SimpleJWT (token-based authentication)  
- django-filters  

---

## 📁 Project Structure

Store_API/
│
├── config/
│ ├── config/
│ │ ├── settings.py
│ │ ├── urls.py
│ │ └── wsgi.py
│ └── manage.py
│
└── shop/
├── models.py
├── serializers.py
├── views.py
├── urls.py
├── exceptions.py
├── exception_handler.py
└── permissions.py

---

## 🔐 Authentication

**JWT Endpoints**
| Method | Endpoint | Description |
|--------|-----------|--------------|
| `POST` | `/api/auth/token/` | Obtain access + refresh tokens |
| `POST` | `/api/auth/token/refresh/` | Refresh access token |
| `POST` | `/api/auth/token/verify/` | Verify token validity |

---

## 🛒 Main Endpoints

### **Products & Categories (admin only)**
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/products/` | List products |
| `POST` | `/api/products/` | Create product |
| `GET` | `/api/categories/` | List categories |
| `POST` | `/api/categories/` | Create category |

---

### **Cart**
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/cart/` | Get active cart |
| `POST` | `/api/cart/items/` | Add product to cart |
| `PATCH` | `/api/cart/items/<id>/` | Update quantity |
| `DELETE` | `/api/cart/items/<id>/` | Remove item |
| `POST` | `/api/cart/clear/` | Clear the entire cart |
| `POST` | `/api/orders/checkout/` | Create new order from cart |

---

### **Orders**
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/orders/` | List user orders |
| `GET` | `/api/orders/<id>/` | Get order details |
| `POST` | `/api/orders/<id>/pay/` | Mark order as paid |
| `POST` | `/api/orders/<id>/cancel/` | Cancel order (and restock items) |

---

## ⚙️ Installation & Setup
---

## 🔐 Authentication

**JWT Endpoints**
| Method | Endpoint | Description |
|--------|-----------|--------------|
| `POST` | `/api/auth/token/` | Obtain access + refresh tokens |
| `POST` | `/api/auth/token/refresh/` | Refresh access token |
| `POST` | `/api/auth/token/verify/` | Verify token validity |

---

## 🛒 Main Endpoints

### **Products & Categories (admin only)**
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/products/` | List products |
| `POST` | `/api/products/` | Create product |
| `GET` | `/api/categories/` | List categories |
| `POST` | `/api/categories/` | Create category |

---

### **Cart**
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/cart/` | Get active cart |
| `POST` | `/api/cart/items/` | Add product to cart |
| `PATCH` | `/api/cart/items/<id>/` | Update quantity |
| `DELETE` | `/api/cart/items/<id>/` | Remove item |
| `POST` | `/api/cart/clear/` | Clear the entire cart |
| `POST` | `/api/orders/checkout/` | Create new order from cart |

---

### **Orders**
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/orders/` | List user orders |
| `GET` | `/api/orders/<id>/` | Get order details |
| `POST` | `/api/orders/<id>/pay/` | Mark order as paid |
| `POST` | `/api/orders/<id>/cancel/` | Cancel order (and restock items) |

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/Deadrizz/store-api-django-project.git
cd store-api-django-project/config

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver
API will be available at:
👉 http://127.0.0.1:8000/
Interactive docs (Swagger / Redoc) are automatically generated via drf-spectacular:

Swagger UI: http://127.0.0.1:8000/api/docs/

Redoc: http://127.0.0.1:8000/api/redoc/
Every API error returns a consistent JSON structure:

{
  "detail": "Not enough stock.",
  "key": "quantity",
  "available": 3,
  "status_code": 400
}
🧠 Example Workflow

Obtain JWT token with /api/auth/token/

Create a category and a product (admin)

Add product to cart

Checkout → creates order

Pay the order → status changes to PAID
🧑‍💻 Author

Stanislav Simutin
GitHub: @Deadrizz

Project: Store API Django Project
🏁 License

This project is released under the MIT License.
Feel free to use, modify, and share for learning or development purposes.
