# 🏪 Store API (Django + DRF)

![Tests](https://github.com/Deadrizz/store-api-django-project/actions/workflows/ci.yml/badge.svg)

A simple but production-oriented e-commerce backend built with **Django** and **Django REST Framework**.

The project provides:

- product catalog with search, ordering and pagination
- authenticated shopping cart
- order checkout with stock validation
- JWT authentication
- automated tests, Docker setup and CI (GitHub Actions)

---

## 🚀 Features

### Products
- List all products with pagination: `GET /api/products/`
- Search by name: `GET /api/products/?search=Macbook`
- Ordering by price: `GET /api/products/?ordering=-price`
- Only active products are returned
- Stock is respected when creating orders

### Cart
- Only available for authenticated users (JWT)
- Endpoints (example naming, adjust if needed):
  - `POST /api/cart/items/` – add item to cart
  - `GET /api/cart/items/` – list cart items
- Validates:
  - only existing products can be added
  - quantity must not exceed stock

### Orders
- `POST /api/orders/checkout/`
  - Creates a new order from the current user’s cart
  - Validates that:
    - user is authenticated
    - cart is not empty
    - there is enough stock for each product
  - Decreases product stock and clears the user’s cart
  - Calculates total order price (sum over `quantity * price`)

### Authentication (JWT)
- Implemented via `djangorestframework-simplejwt`
- Endpoints (typical configuration):
  - `POST /api/auth/token/` – obtain access & refresh tokens
  - `POST /api/auth/token/refresh/` – refresh access token
- Protected endpoints (cart, orders) require `Authorization: Bearer <access_token>`

### Unified error responses
- Custom exception is used to return consistent error JSON with a `key` field
  (for example: `"quantity"`, `"cart"`, `"product"`).
- This makes it easier to handle errors on frontend side.

### Automated tests
- Tests implemented with:
  - `pytest`
  - `pytest-django`
  - `model_bakery`
- Covered scenarios:
  - products list (empty and with data)
  - pagination, search, ordering by price
  - cart access (unauthenticated vs authenticated)
  - adding items to cart
  - making orders, empty cart case, total price, clearing cart after checkout

---

## 🧰 Tech stack

- **Backend:** Django 5, Django REST Framework
- **Auth:** djangorestframework-simplejwt (JWT)
- **Database:** PostgreSQL
- **Schema & docs:** drf-spectacular (+ optional Swagger UI)
- **Testing:** pytest, pytest-django, model-bakery
- **Containerization:** Docker, docker-compose
- **CI:** GitHub Actions (run tests on each push to `main`)

---

## 📁 Project structure (simplified)

```text
store-api-django-project/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                  # not committed, see .env example below
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions workflow (pytest + Postgres)
├── conftest.py           # global pytest fixtures (APIClient, product factory, etc.)
└── config/
    ├── manage.py
    ├── pytest.ini
    ├── config/
    │   ├── settings.py
    │   ├── urls.py
    │   └── ...
    └── shop/
        ├── models.py
        ├── serializers.py
        ├── views.py
        ├── urls.py
        └── tests/
            ├── test_products.py
            ├── test_cart.py
            └── test_orders.py
⚙️ Environment variables
The project uses environment variables (e.g. via .env file).

Example .env:

env
Копировать код
# PostgreSQL
POSTGRES_DB=store_db
POSTGRES_USER=store_user
POSTGRES_PASSWORD=store_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Django
SECRET_KEY=dev-secret-key-change-me
DEBUG=True
For Docker / docker-compose the POSTGRES_HOST is overridden to db (the name of the database service).

💻 Local development (without Docker)
Requirements:

Python 3.12

PostgreSQL running locally

virtualenv (recommended)

1. Clone the repository
bash
Копировать код
git clone https://github.com/Deadrizz/store-api-django-project.git
cd store-api-django-project
2. Create and activate virtual environment
bash
Копировать код
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# or:
# .venv\Scripts\activate       # Windows
3. Install dependencies
bash
Копировать код
pip install --upgrade pip
pip install -r requirements.txt
4. Configure .env
Create .env in the project root (see example above) and ensure your local PostgreSQL
is configured with matching POSTGRES_* values.

5. Apply migrations
bash
Копировать код
cd config
python manage.py migrate
6. Create superuser (optional, for admin panel)
bash
Копировать код
python manage.py createsuperuser
7. Run development server
bash
Копировать код
python manage.py runserver
The API will be available at:
http://127.0.0.1:8000/

🐳 Running with Docker
The project ships with a docker-compose.yml that starts:

web – Django application

db – PostgreSQL

1. Build and start services
From the repository root:

bash
Копировать код
docker compose up --build
This will:

build the Django image,

start PostgreSQL,

wait until the DB is ready,

run migrations,

start the development server at 0.0.0.0:8000.

2. Run management commands inside the container
Example: create superuser:

bash
Копировать код
docker compose exec web python manage.py createsuperuser
🧪 Running tests
Locally
From the config directory:

bash
Копировать код
cd config
pytest -v
In CI (GitHub Actions)
On each push to the main branch, a GitHub Actions workflow:

starts a PostgreSQL service,

installs dependencies,

applies migrations,

runs pytest -v.

You can see the current status in the Actions tab or via the badge at the top of this README.

📚 API documentation
The project uses drf-spectacular to generate OpenAPI schema.

Typical setup (may slightly differ depending on your urls):

OpenAPI schema: GET /api/schema/

Swagger UI: /api/schema/swagger-ui/

ReDoc: /api/schema/redoc/

Adjust the paths here according to your urls.py if needed.

✅ Possible improvements
Some ideas for future work:

add more detailed tests for edge cases (stock edge cases, permissions, etc.)

extend product model (categories, images, descriptions)

add user profile and order history endpoints

integrate rate limiting and throttling

deploy to a public hosting (Render, Railway, etc.)

🙋 About the project
This project was built as a learning / portfolio backend to practice:

Django REST Framework best practices,

writing tests with pytest and model_bakery,

working with Docker and docker-compose,

setting up CI with GitHub Actions.

Feel free to fork, open issues or suggestions.
🧑‍💻 Author

Stanislav Simutin
GitHub: @Deadrizz

Project: Store API Django Project
🏁 License

This project is released under the MIT License.
Feel free to use, modify, and share for learning or development purposes.
