# Sheebmart E-Commerce Website

A modern responsive fashion/lifestyle e-commerce project built with Django, Bootstrap 5, JavaScript and MySQL.

## 1. Create environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Database

For the quickest local start, leave `DB_ENGINE=sqlite`.

For MySQL:

1. Create a database named `sheebmart`.
2. Copy `.env.example` to `.env`.
3. Set `DB_ENGINE=mysql`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.
4. Start Django normally; the project loads `.env` automatically.

Example MySQL:
```sql
CREATE DATABASE sheebmart CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

> This project reads environment variables directly. It does not require python-dotenv.

## 3. Create migrations

```bash
python manage.py makemigrations products cart orders
python manage.py migrate
```

## 4. Create admin user

```bash
python manage.py createsuperuser
```

## 5. Add demo data

```bash
python manage.py seed_demo_data
```

This creates the eight categories and sample products.

## 6. Run

```bash
python manage.py runserver
```

Open:
- Store: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Main flow

Home → Shop → Product Details → Add to Cart → Login → Address → Summary → Place Order → Success → My Orders

## Notes

- Guest carts use Django session storage.
- Logged-in carts use database models.
- JavaScript localStorage is used as a frontend cart-change marker while the authoritative cart is kept in Django/session or database.
- Payment is intentionally a demo placeholder; no real payment gateway is integrated.
- Product images in the demo data use remote Unsplash URLs. Replace them with your own product image URLs or an ImageField/media setup for production.
