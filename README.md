<p align="center">
  <img src="https://img.shields.io/badge/Vue_3-4FC08D?logo=vuedotjs&logoColor=white" alt="Vue 3"/>
  <img src="https://img.shields.io/badge/Django_6-092E20?logo=django&logoColor=white" alt="Django 6"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white" alt="Vite"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwindcss&logoColor=white" alt="Tailwind CSS"/>
  <br/>
  <img src="https://img.shields.io/badge/build-passing-22c55e?logo=checkmarx"/>
  <img src="https://img.shields.io/badge/coverage-15_tests-06b6d4"/>
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
│   │   ├── forms.py                # ContactForm, TaskForm
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
pip install django djangorestframework django-cors-headers

cd backend
python manage.py migrate
python manage.py seed_tasks
python manage.py create_admin
python manage.py runserver 0.0.0.0:8000
```

---

## 🌐 Django Routes

| Path | View | Description |
|------|------|-------------|
| `/` | `home` | Homepage with task stats & recent tasks |
| `/login/` | `LoginView` | Login page |
| `/logout/` | `LogoutView` | Logout (POST-only) |
| `/accounts/register/` | `register` | User registration |
| `/tasks/` | `task_list` | Full task table with status badges (login required) |
| `/tasks/search/` | `task_search` | AJAX search JSON endpoint (login required) |
| `/tasks/create/` | `task_create` | New task form (login required) |
| `/tasks/<id>/` | `task_detail` | Task detail page (login required) |
| `/tasks/<id>/edit/` | `task_update` | Edit task form (login required) |
| `/tasks/<id>/delete/` | `task_delete` | Delete confirmation (login required) |
| `/tasks/<id>/toggle/` | `task_toggle` | Toggle completed (POST, login required) |
| `/contact/` | `contact` | Contact form with messages |
| `/shop/`, `/faq/`, `/about/` | `page_placeholder` | Placeholder pages |
| `/robots.txt` | `robots_txt` | Robots exclusion |
| `/humans.txt` | `humans_txt` | Credits |
| `/sitemap.xml` | `sitemap_xml` | XML sitemap |
| `/admin/` | Django Admin | Dark-themed admin |

### Authentication

Task management requires login. Use the admin credentials below or register at `/accounts/register/`.

**Admin credentials:**
- **Username:** `admin`
- **Password:** `admin123`

---

## 🗄️ Data Models

### website app
- **Task** — title, description, completed, timestamps
- **ContactMessage** — name, email, message, timestamp

### api app
- **Category** — name, slug
- **Product** — slug (PK), name, price, category, image, rating, specs, stock
- **Order** — email, name, address, status, gift card
- **OrderItem** — product, name, price, quantity, item_type
- **BackInStockRequest** — product, email
- **ContactMessage** — name, email, message

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

## 📝 Management Commands

```bash
python manage.py seed_tasks      # Create 5 sample tasks
python manage.py seed_data        # Create 21 products
python manage.py create_admin     # Create admin user
python manage.py count_models     # Show record counts
python manage.py list_tasks       # Show all tasks in terminal
python manage.py reset_tasks      # Delete & reseed tasks
python manage.py health_check     # Database connectivity test
```

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

```bash
python backend/manage.py test website
```

---

## 📦 Dependencies

**Frontend:** Vue 3, Vue Router, Vite, Tailwind CSS  
**Backend:** Django 6.0.6, Django REST Framework 3.17.1, django-cors-headers 4.9.0  
**Python:** 3.14.5  
**Database:** SQLite
