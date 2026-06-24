<p align="center">
  <img src="https://img.shields.io/badge/Vue_3-4FC08D?logo=vuedotjs&logoColor=white" alt="Vue 3"/>
  <img src="https://img.shields.io/badge/Django_6-092E20?logo=django&logoColor=white" alt="Django 6"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white" alt="Vite"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwindcss&logoColor=white" alt="Tailwind CSS"/>
  <br/>
  <img src="https://img.shields.io/badge/build-passing-22c55e?logo=checkmarx"/>
  <img src="https://img.shields.io/badge/coverage-27_tests-06b6d4"/>
  <img src="https://img.shields.io/badge/commits-290+-blue"/>
  <img src="https://img.shields.io/badge/license-MIT-blue"/>
</p>

<h1 align="center">🖥️ TechStore — Full Stack Storefront</h1>

<p align="center">
  Vue 3 SPA storefront + Django 6 MVT dashboard &amp; REST API<br/>
  Composition API · Vue Router · Tailwind CSS · Vite · Django REST Framework
</p>

---

## 📁 Project Structure

```
📁 .
├── 📦 frontend/                    # Vue 3 + Vite SPA
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── style.css
│       ├── router/index.js
│       ├── data/products.js
│       ├── composables/            # 11 composables
│       ├── components/             # 20+ components
│       └── views/                  # 17 route pages
│
├── 📁 backend/                     # Django 6 project
│   ├── manage.py
│   ├── config/                     # Project settings, root URLconf
│   ├── website/                    # MVT app (templates, forms, views)
│   │   ├── models.py               # Task, ContactMessage, Comment
│   │   ├── views.py                # 14 function views
│   │   ├── forms.py                # RegisterForm, ContactForm, TaskForm, CommentForm
│   │   ├── admin.py                # Custom admin config + actions
│   │   ├── middleware.py           # MaintenanceModeMiddleware
│   │   ├── context_processors.py   # site_context
│   │   ├── templatetags/           # status_badge, time_ago, etc.
│   │   ├── management/commands/    # 5 custom commands
│   │   ├── templates/website/      # 12 templates
│   │   └── static/website/         # CSS, JS, favicon
│   └── api/                        # REST API app
│       ├── models.py               # Category, Product, Order, etc.
│       ├── serializers.py
│       ├── views.py
│       └── admin.py
│
├── 📄 .gitignore
├── 📄 AGENTS.md
└── 📄 README.md
```

---

## 🏗️ Deployment Options

This project runs a Django backend serving both a REST API and a server-rendered MVT website (task manager, contact form, auth). There are three ways to deploy it, depending on your needs.

### Architecture Overview

```
                         ┌──────────────┐
 Browser ──HTTP/HTTPS──► │  Nginx       │
                         │  (optional)  │
                         └──────┬───────┘
                                │
                    ┌───────────▼───────────┐
                    │  Gunicorn (WSGI)      │
                    │  ─ or ─              │
                    │  runserver (dev)      │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Django Backend        │
                    │  · MVT Templates       │
                    │  · REST API (/api/)    │
                    │  · Admin (/admin/)     │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │  SQLite Database       │
                    │  (backend/db.sqlite3)  │
                    └───────────────────────┘
```

**Single-server setup** — no external database or separate frontend build step required. The Vue frontend lives in a separate directory (`src/`, `dist/`) but is not served by Django; it uses mock data and runs independently via `npm run dev`.

---

## 🚀 Quick Start

### Vue Frontend

```bash
npm install
npm run dev       # → http://localhost:5173
npm run build     # Production build → dist/
```

### Django Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

cd backend
python manage.py migrate
python manage.py seed_tasks           # 10 tasks with comments
python manage.py seed_data             # 21 products across 3 categories
python manage.py create_admin          # Creates user: admin / admin123
python manage.py runserver 0.0.0.0:8000
```

---

### Local Deployment (Viewing on Your Network)

To make the site accessible to other devices on your LAN (phone, tablet, other computers):

```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

**From another device:** open `http://<YOUR_IP>:8000/` in a browser.

> **Find your IP:** run `ip addr show | grep inet` (Linux), `ipconfig getifaddr en0` (macOS), or `ipconfig` (Windows).

| URL | What you see |
|-----|-------------|
| `http://localhost:8000/` | Homepage with task stats & recent tasks |
| `http://localhost:8000/tasks/` | Task manager (login required) |
| `http://localhost:8000/admin/` | Django admin panel |
| `http://localhost:8000/api/health/` | API health check endpoint |

---

### Production Deployment (Gunicorn)

For a proper production setup, swap `runserver` for **Gunicorn**:

```bash
pip install gunicorn
cd backend
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**Recommended:** place behind **Nginx** (see below) for static file serving, SSL termination, and security headers.

---

### Nginx Reverse Proxy

Place Nginx in front of Gunicorn to serve static files and handle HTTPS:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/backend/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

First collect static files:
```bash
python manage.py collectstatic --noinput
```

---

### Docker Deployment

Run the entire backend in a container:

```bash
# Build & start
docker compose up --build

# The site is available at http://localhost:8000
```

Or pull and run with a single container:
```bash
docker build -t techstore-backend backend/
docker run -d -p 8000:8000 -v $(pwd)/backend/db.sqlite3:/app/db.sqlite3 techstore-backend
```

---

### Deployment Quick Reference

| Step | Command |
|------|---------|
| Install dependencies | `pip install -r backend/requirements.txt` |
| Run migrations | `python backend/manage.py migrate` |
| Seed sample data | `python backend/manage.py seed_tasks && python backend/manage.py seed_data` |
| Create admin user | `python backend/manage.py create_admin` |
| Collect static files | `python backend/manage.py collectstatic --noinput` |
| Start development server | `python backend/manage.py runserver 0.0.0.0:8000` |
| Start Gunicorn | `gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4` |
| Verify health | `curl http://localhost:8000/api/health/` |

---

### Production Checklist

Before deploying to production, verify these items:

- [ ] **`DEBUG = False`** in `config/settings.py`
- [ ] **`SECRET_KEY`** set via environment variable (not hardcoded)
- [ ] **`ALLOWED_HOSTS`** set to your domain(s), e.g. `["yourdomain.com", "www.yourdomain.com"]`
- [ ] **`STATIC_ROOT`** collected: `python manage.py collectstatic --noinput`
- [ ] **HTTPS** enabled via reverse proxy (Nginx + Let's Encrypt)
- [ ] **Database backup** strategy in place (SQLite is a single file — easy to cron-copy)
- [ ] **`MAINTENANCE_MODE = False`** (toggle to `True` to show a maintenance page)

### Environment Variables

The following variables can be set in your shell or in a `.env` file (loaded via `python-dotenv`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | *(hardcoded dev key)* | Production secret key (generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`) |
| `DJANGO_DEBUG` | `True` | Set to `False` in production |
| `DJANGO_ALLOWED_HOSTS` | `*` | Comma-separated list of allowed domain names |
| `DJANGO_PORT` | `8000` | Port for the dev server |
| `MAINTENANCE_MODE` | `False` | Set to `True` to display maintenance page |

### Network URLs Cheat Sheet

| Context | URL | Purpose |
|---------|-----|---------|
| Local dev | `http://localhost:8000/` | Your own machine |
| LAN access | `http://192.168.x.x:8000/` | Other devices on your network |
| Production | `https://yourdomain.com/` | Public internet |
| Admin panel | `http://localhost:8000/admin/` | Django admin (all environments) |
| API health | `http://localhost:8000/api/health/` | Quick connectivity check |

---

## 🌐 Django Routes

| Path | View | Description |
|------|------|-------------|
| `/` | `home` | Homepage with task stats, comment count & recent tasks |
| `/login/` | `LoginView` | Login page |
| `/logout/` | `LogoutView` | Logout (POST-only) |
| `/accounts/register/` | `register` | User registration with auto-login |
| `/tasks/` | `task_list` | Full task table with status badges (login required) |
| `/tasks/search/` | `task_search` | AJAX search JSON endpoint (login required) |
| `/tasks/create/` | `task_create` | New task form (login required) |
| `/tasks/<id>/` | `task_detail` | Task detail page (login required) |
| `/tasks/<id>/edit/` | `task_update` | Edit task form (login required) |
| `/tasks/<id>/delete/` | `task_delete` | Delete confirmation (login required) |
| `/tasks/<id>/toggle/` | `task_toggle` | Toggle completed (POST, login required) |
| `/tasks/<id>/comment/` | `add_comment` | Add comment (POST, login required) |
| `/dashboard/` | `admin_dashboard` | Admin dashboard with stats, recent orders/tasks, quick actions (staff only) |
| `/contact/` | `contact` | Contact form with messages |
| `/shop/`, `/faq/`, `/about/` | `page_placeholder` | Placeholder pages |
| `/robots.txt` | `robots_txt` | Robots exclusion |
| `/humans.txt` | `humans_txt` | Credits |
| `/sitemap.xml` | `sitemap_xml` | XML sitemap |
| `/admin/` | Django Admin | Dark-themed admin with full CRUD |
| `/api/health/` | `health_check` | REST API health check |

### Authentication

Task management requires login. The registration flow:
1. Visit `/accounts/register/` with username, email, and password
2. On success, user is **auto-logged in** and redirected to `/tasks/`
3. Fields validated inline with per-field error messages
4. Email is required and validated for spaces
5. Logout requires POST (prevents CSRF-based logout)

---

> **Note:** The Vue frontend uses static mock data from `src/data/products.js`. The Django backend has its own product catalog managed via admin. They share the same schema but are independent data stores — the Django admin is the source of truth for backend data, while the Vue SPA renders its own fixed product list.

---

## 🗄️ Data Models

### website app
| Model | Fields | Admin Features |
|-------|--------|---------------|
| **Task** | title, description, completed, created_at, updated_at | Bulk mark done/pending, CSV export, inline edit, search, filter, date drill-down |
| **Comment** | task (FK), author, body, created_at, updated_at | Bulk delete, filter by task/date, clickable task link, body preview |
| **ContactMessage** | name, email, message, created_at | Read-only, bulk delete old messages, search by name/email/message |

### api app
| Model | Fields | Admin Features |
|-------|--------|---------------|
| **Category** | name, slug | Slug auto-populated from name, search by name |
| **Product** | slug (PK), name, price, category (FK), image, rating, specs (JSON), stock, timestamps | Filter by category/rating, search by name/description, slug auto-populated |
| **Order** | email, name, address, status, gift_card, created_at | Inline order items, filter by status, search by name/email |
| **OrderItem** | order (FK), product (FK), name, price, quantity, item_type | Inline in Order admin |
| **BackInStockRequest** | product (FK), email, created_at | Search by email/product, date drill-down |

---

## 🎛️ Admin Panel

Access the admin interface at **`http://localhost:8000/admin/`** after starting the server.

### Login
```bash
# Create the admin user (first time only):
python manage.py create_admin

# Or create a custom superuser:
python manage.py createsuperuser
```

**Default admin credentials:**
- **Username:** `admin`
- **Password:** `admin123`

### Managing Data via Admin

#### Adding a Product
1. Go to `/admin/api/product/add/`
2. Fill in: **Slug** (auto-filled from name), **Name**, **Price**, **Category** (select or `+` to add new), **Description**, **Image URL**, **Rating**, **Stock**
3. **Specs** - enter as a JSON list, e.g. `["RTX 5070 12GB", "32GB DDR5"]`
4. Click **Save**

#### Adding a Category
1. Go to `/admin/api/category/add/`
2. Enter **Name** — **Slug** fills automatically
3. Click **Save**

#### Managing Orders
1. Go to `/admin/api/order/` — see all orders with status, search by customer name/email
2. Click an order to view/edit details
3. **Add items inline** — scroll to "Order items" section, click "Add another Order Item"
4. **Update status** — choose from: Placed, Processing, Shipped, Out for delivery, Delivered

#### Managing Tasks
Custom admin actions available:
- **Mark selected as completed** — bulk mark done
- **Mark selected as pending** — bulk reopen
- **Export selected as CSV** — download task data
- **Inline editing** — toggle completed checkbox directly in list view
- **Edit/Create** — structured form with collapsible timestamps section

#### Managing Comments
- **Search** — by author, body content, or task title
- **Filter** — by creation date or task
- **Bulk delete** — select comments and choose "Delete selected comments"
- **Task link** — click to jump directly to the commented task

#### Managing Contact Messages
- Read-only (created via the public contact form)
- **Delete old messages** action — removes messages older than 30 days

---

## 👤 User-Facing Features

### Task Management (requires login)
| Feature | How To |
|---------|--------|
| **View tasks** | `/tasks/` — table with status badges, search bar |
| **Live search** | Type in the search box — results appear instantly via AJAX |
| **Create task** | `/tasks/create/` — title + optional description |
| **Edit task** | Click edit icon or "Edit Task" on detail page |
| **Toggle status** | Click the checkmark/x button in the table |
| **Delete task** | Click trash icon, confirm on next page |
| **View details** | Click task title for full view with timestamps |
| **Add comment** | Scroll to bottom of task detail page, enter name + comment |

### Registration & Login
1. Go to `/accounts/register/`
2. Enter username, email, and password (auto-login on success)
3. Or go to `/login/` if you already have an account
4. Logout via POST (button in header)

### Contact
- `/contact/` — public form; messages visible to admins only

---

## 🔍 Database Access (SQLite)

The database file is at **`backend/db.sqlite3`**. You have several ways to inspect and query it:

### Option 1: Django Shell (Recommended)
```bash
python manage.py shell

# Example queries:
>>> from website.models import *
>>> Task.objects.count()
>>> Task.objects.filter(completed=True)
>>> Comment.objects.filter(author="Alice")
>>> ContactMessage.objects.all()

>>> from api.models import *
>>> Category.objects.all()
>>> Product.objects.filter(price__lt=100)
>>> Product.objects.filter(stock=0)           # Out of stock items
>>> Order.objects.filter(status="placed")
```

### Option 2: Django `dbshell`
```bash
python manage.py dbshell
# SQLite prompt — run raw SQL:
.tables
SELECT * FROM website_task;
SELECT * FROM api_product WHERE price < 100;
SELECT COUNT(*) FROM website_comment;
```

### Option 3: Direct SQLite (when Django isn't running)
```bash
sqlite3 backend/db.sqlite3
.tables
SELECT title, completed FROM website_task;
```

### Option 4: GUI Browser (DB Browser for SQLite)
Install [DB Browser for SQLite](https://sqlitebrowser.org/), open `backend/db.sqlite3`, and browse/edit tables visually.

### Option 5: Management Commands
```bash
python manage.py count_models     # Show record counts for all models
python manage.py list_tasks       # List all tasks with status in terminal
python manage.py health_check     # Verify database connection
```

---

## 🚀 Seeding Sample Data

```bash
# Seed 10 tasks with comments (1-4 comments each):
python manage.py seed_tasks

# Seed 21 products across categories:
python manage.py seed_data

# Create admin user:
python manage.py create_admin
```

### Full Startup Sequence
```bash
source .venv/bin/activate
cd backend
python manage.py migrate
python manage.py seed_tasks
python manage.py seed_data
python manage.py create_admin
python manage.py runserver 0.0.0.0:8000
```

---

## 📝 Management Commands

| Command | Description |
|---------|-------------|
| `seed_tasks` | Create 10 sample tasks with comments |
| `seed_data` | Create 21 products with categories |
| `create_admin` | Create admin user (`admin` / `admin123`) |
| `count_models` | Show record counts (Tasks, Comments, Contact Messages) |
| `list_tasks` | Show all tasks in terminal |
| `reset_tasks` | Delete all tasks and reseed |
| `health_check` | Database connectivity test |

---

## 🧩 Composables (Vue)

| Composable | Purpose |
|-----------|---------|
| `useCart` | Cart with localStorage, upgrades, membership |
| `useToast` | Toast notifications |
| `useFavorites` | Wishlist with localStorage |
| `useRecentlyViewed` | Last 6 products |
| `useTheme` | Dark/light toggle |
| `useLiveVisitorCount` | Fluctuating counter |
| `useSalesNotifications` | Simulated live sales |
| `useFreeShipping` | Progress bar |
| `useCounter` | Counter feature |
| `useRouteLoading` | Skeleton states |
| `useLoadingBar` | Top progress bar |

---

## 🎨 Styling

- **Tailwind CSS** with custom cyan/slate theme
- **Fonts:** Inter (sans), JetBrains Mono (mono)
- **Dark mode:** Class-based with localStorage persistence
- **Django templates:** Tailwind Play CDN (no build step)
- **Custom CSS:** Scrollbar, hero glow, keyframes, print styles

---

## ♿ Accessibility

- Skip-to-content link
- ARIA landmarks & `aria-current="page"`
- Keyboard navigation with visible focus rings
- Semantic heading hierarchy
- `focus-visible` outlines
- Screen reader labels on icon buttons

---

## 🧪 Running Tests

### Test Suite

```bash
# Run all website app tests (12 tests):
python backend/manage.py test website

# Run with verbose output:
python backend/manage.py test website --verbosity=2

# Run a specific test class:
python backend/manage.py test website.tests.RegisterViewTests

# Run a single test method:
python backend/manage.py test website.tests.RegisterViewTests.test_register_success
```

### What's Tested

| Test Class | Tests | Coverage |
|------------|-------|----------|
| `TaskViewTests` | 7 | Task CRUD, toggle, search, comment flow, auth guards |
| `RegisterViewTests` | 5 | Registration success, auto-login, duplicate user, invalid email, GET form |

### CI Quick Reference

```bash
# Full test suite (exit code 0 = all pass):
python backend/manage.py test website --verbosity=2 && echo "ALL PASSED"

# Check for pending migrations:
python backend/manage.py makemigrations --check --dry-run
```

---

## 📦 Dependencies

**Frontend:** Vue 3, Vue Router, Vite, Tailwind CSS  
**Backend:** Django 6.0.6, Django REST Framework 3.17.1, django-cors-headers 4.9.0  
**Python:** 3.14.5  
**Database:** SQLite
