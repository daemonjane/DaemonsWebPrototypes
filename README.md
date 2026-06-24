<p align="center">
  <img src="https://img.shields.io/badge/Vue_3-4FC08D?logo=vuedotjs&logoColor=white" alt="Vue 3"/>
  <img src="https://img.shields.io/badge/Django_6-092E20?logo=django&logoColor=white" alt="Django 6"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white" alt="Vite"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwindcss&logoColor=white" alt="Tailwind CSS"/>
  <br/>
  <img src="https://img.shields.io/badge/build-passing-22c55e?logo=checkmarx"/>
  <img src="https://img.shields.io/badge/license-MIT-blue"/>
</p>

<h1 align="center">TechStore — Full Stack Storefront</h1>

<p align="center">
  Vue 3 SPA storefront + Django 6 MVT dashboard & REST API<br/>
  Composition API · Vue Router · Tailwind CSS · Vite · Django REST Framework
</p>

---

## Project Structure

```
.
├── src/                          # Vue 3 + Vite SPA (root level)
│   ├── main.js
│   ├── App.vue
│   ├── style.css
│   ├── router/index.js
│   ├── utils/
│   │   └── api.js                # HTTP client (CSRF-aware fetch wrapper)
│   ├── composables/              # useCart, useUser, useFavorites, etc.
│   ├── components/               # Header, ProductCard, CartDrawer, etc.
│   └── views/                    # Login, Register, Shop, Cart, Profile, etc.
│
├── backend/                      # Django 6 project
│   ├── manage.py
│   ├── .env                      # Environment variables (email, secrets)
│   ├── .env.example
│   ├── config/                   # Django settings, root URLconf, wsgi
│   ├── website/                  # MVT app (templates, forms, views, models)
│   ├── api/                      # REST API app (models, views, serializers)
│   └── requirements.txt
│
├── dist/                         # Built SPA (served by Django in production)
├── docker-compose.yml
├── .gitignore
├── AGENTS.md
└── README.md
```

---

## Quick Start

### 1. Backend (Django)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_tasks          # 10 sample tasks with comments
python manage.py seed_data           # 21 products across 3 categories
python manage.py create_admin        # Creates admin / admin123
python manage.py runserver 0.0.0.0:8000
```

### 2. Frontend (Vue SPA) — development mode

In a separate terminal:

```bash
npm install
npm run dev        # → http://localhost:5173 (hot-reload)
```

The Vite dev server proxies `/api/` requests to Django at `localhost:8000`.

### 3. Production build (Vue served by Django)

```bash
npm run build                          # outputs to dist/
# Django serves dist/index.html at every non-API path
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
cp backend/.env.example backend/.env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | *(dev key)* | Generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| `DJANGO_DEBUG` | `True` | Set `False` in production |
| `DJANGO_ALLOWED_HOSTS` | `*` | Comma-separated domains |
| `MAINTENANCE_MODE` | `False` | Shows maintenance page when `True` |
| `EMAIL_BACKEND` | `console` | Switch to `smtp` for real sending |
| `EMAIL_HOST` | `localhost` | SMTP server (e.g. `smtp.gmail.com`) |
| `EMAIL_PORT` | `587` | SMTP port |
| `EMAIL_USE_TLS` | `True` | TLS for SMTP |
| `EMAIL_HOST_USER` | — | SMTP username |
| `EMAIL_HOST_PASSWORD` | — | SMTP password (Gmail: use App Password) |
| `DEFAULT_FROM_EMAIL` | `noreply@techstore.local` | From address for outgoing mail |
| `CONTACT_TO_EMAIL` | `admin@techstore.local` | Where contact form submissions go |

Example Gmail SMTP config:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=mail.charbelelias05@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=mail.charbelelias05@gmail.com
CONTACT_TO_EMAIL=mail.charbelelias05@gmail.com
```

---

## How the SPA Connects to Django

The Vue SPA communicates with Django via a REST API at `/api/`. Authentication uses **session cookies** (same-origin).

### CSRF Protection

All unsafe HTTP methods (POST, PUT, PATCH, DELETE) send the `X-CSRFToken` header:

1. On app start, `ensureCSRF()` fetches `GET /api/auth/csrf/` to set the `csrftoken` cookie
2. The API client reads the cookie and includes it as `X-CSRFToken` on every unsafe request
3. Django REST Framework's `SessionAuthentication` validates the token server-side

---

## API Reference

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | Create account + auto-login |
| `POST` | `/api/auth/login/` | Authenticate, get session |
| `POST` | `/api/auth/logout/` | Destroy session |
| `GET` | `/api/auth/profile/` | Current user data |
| `PATCH` | `/api/auth/profile/` | Update email, username, bio, etc. |
| `GET` | `/api/auth/csrf/` | Get CSRF token (sets cookie) |

**Login request:**
```json
{ "username": "admin", "password": "admin123" }
```

**Login response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@techstore.dev",
  "is_staff": true,
  "is_superuser": true,
  "profile": { "bio": "", "location": "", "phone": "", "avatar_url": "" }
}
```

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products/search/?q=&category=` | Search/filter products |

### Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cart/` | Get current cart |
| `POST` | `/api/cart/add/` | Add item to cart |
| `PATCH` | `/api/cart/item/<id>/` | Update item quantity |
| `DELETE` | `/api/cart/item/<id>/` | Remove item from cart |
| `POST` | `/api/cart/clear/` | Empty the entire cart |
| `POST` | `/api/cart/merge/` | Merge localStorage items after login |

**Add to cart:**
```json
{ "product_slug": "nvidia-rtx-5070", "quantity": 1, "name": "RTX 5070", "price": 549.99, "image": "" }
```

### Wishlist

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/wishlist/` | List favorited product slugs |
| `POST` | `/api/wishlist/toggle/` | Add/remove favorite |
| `GET` | `/api/wishlist/check/<slug>/` | Check if product is favorited |

**Toggle:**
```json
{ "slug": "nvidia-rtx-5070" }
```

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/orders/` | List user's orders |
| `GET` | `/api/orders/<id>/` | Order detail |
| `POST` | `/api/orders/checkout/` | Place order from cart |

**Checkout:**
```json
{ "address": "123 Main St, City", "name": "Jane Doe", "email": "jane@example.com" }
```

---

## Frontend Login Flow

From `Login.vue`:

```
POST /api/auth/login/  ───►  authenticate + login()
        │
        ▼
refresh() — GET /api/auth/profile/  ───►  returns user data
        │
        ├── syncCart()     — mergeLocalIntoServer() → POST /api/cart/merge/
        │                     then init() → GET /api/cart/
        │
        └── syncWishlist() — init() → GET /api/wishlist/
```

---

## MVT Website Routes (server-rendered Django templates)

| Path | Description |
|------|-------------|
| `/` | Homepage |
| `/login/` | Login |
| `/logout/` | Logout (POST) |
| `/accounts/register/` | Registration |
| `/tasks/` | Task manager (login required) |
| `/tasks/create/` | Create task |
| `/tasks/<id>/` | Task detail |
| `/tasks/<id>/edit/` | Edit task |
| `/tasks/<id>/delete/` | Delete task |
| `/tasks/<id>/comment/` | Add comment |
| `/tasks/search/` | AJAX task search |
| `/dashboard/` | Admin dashboard (staff only) |
| `/contact/` | Contact form |
| `/newsletter/` | Newsletter subscribe |
| `/admin/` | Django Admin |

---

## Admin Panel

**URL:** `http://localhost:8000/admin/`

**Default credentials:** `admin` / `admin123`

### Managing Products

1. Go to `/admin/api/product/add/`
2. Fill in slug (auto-filled), name, price, category, description, image URL, rating, stock
3. **Specs** — JSON list, e.g. `["RTX 5070 12GB", "32GB DDR5"]`
4. **Save**

### Managing Categories

1. `/admin/api/category/add/`
2. Enter name — slug auto-fills
3. **Save**

### Managing Orders

1. `/admin/api/order/` — view all orders with status
2. Click to edit — add items inline, update status (Placed → Processing → Shipped → Delivered)

### Admin Actions

- **Tasks:** Bulk mark done/pending, CSV export, inline edit
- **Comments:** Bulk delete, filter by task/date
- **Contact Messages:** Read-only, bulk delete old messages

---

## Data Models

### website app

| Model | Key Fields |
|-------|------------|
| `Task` | title, description, completed, created_at, updated_at |
| `Comment` | task (FK), author, body, created_at |
| `ContactMessage` | name, email, message, created_at |
| `NewsletterSubscription` | email, active, created_at |
| `UserProfile` | user (OneToOne), bio, location, phone, avatar_url |

### api app

| Model | Key Fields |
|-------|------------|
| `Category` | name, slug |
| `Product` | slug (PK), name, price, category (FK), image, rating, specs (JSON), stock |
| `Cart` | user (OneToOne), items, total_price, total_items |
| `CartItem` | cart (FK), product (FK), name, price, quantity, image, item_type |
| `Order` | user (FK), email, name, address, status, gift_card_code, gift_card_discount |
| `OrderItem` | order (FK), product (FK), name, price, quantity, item_type |
| `Wishlist` | user (OneToOne), products (M2M) |

---

## Commands

```bash
# Seeding
python manage.py seed_tasks          # 10 tasks with comments
python manage.py seed_data           # 21 products in 3 categories
python manage.py create_admin        # admin / admin123
python manage.py reset_tasks         # Delete all tasks & reseed

# Utilities
python manage.py count_models        # Record counts for all models
python manage.py list_tasks          # Terminal task listing
python manage.py health_check        # DB connectivity test

# Tests
python manage.py test website        # Full test suite
python manage.py test website --verbosity=2
python manage.py test website.tests.TaskViewTests

# Maintenance
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput
```

---

## Database

SQLite at `backend/db.sqlite3`.

```bash
# Django shell
python manage.py shell
>>> from api.models import Product
>>> Product.objects.filter(price__lt=100)

# Raw SQL
python manage.py dbshell
SELECT * FROM api_product WHERE price < 100;

# Direct SQLite
sqlite3 backend/db.sqlite3
.tables
SELECT title, completed FROM website_task;
```

---

## Styling

- **Tailwind CSS** with custom cyan/slate dark theme
- **Fonts:** Inter (sans), JetBrains Mono (mono)
- **Dark mode:** Class-based, persisted in localStorage
- **Django templates:** Tailwind Play CDN (no build step)

---

## Accessibility

- Skip-to-content link
- ARIA landmarks & `aria-current="page"`
- Keyboard navigation with visible focus rings
- Semantic heading hierarchy
- Screen reader labels on icon buttons

---

## Dependencies

**Frontend:** Vue 3, Vue Router, Vite, Tailwind CSS  
**Backend:** Django 6.0.6, DRF 3.17.1, django-cors-headers 4.9.0  
**Python:** 3.14.5  
**Database:** SQLite
