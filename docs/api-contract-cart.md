# Cart API Contract

Documented: 3 Jul 2026

## Table of Contents

1. Architecture Overview
2. Data Models
3. Frontend Contract (useCart.js)
4. API Client Contract (api.js)
5. Backend Django Views
6. OsimartClient Service
7. External Osimart API
8. Data Flows
9. Migration Path

## 1. Architecture Overview

```
Browser (Vue SPA)
  │
  ├─ Header.vue / ProductCard.vue / ProductDetail.vue / ...
  │   call useCart() composable functions
  │
  ├─ src/composables/useCart.js
  │   state management, action dispatch, local fallback
  │   │
  │   ├─ api.osimartCart.*  ──┐
  │   │                       │
  │   └─ api.cart.*  ─────────┤
  │                           │
  ├─ src/utils/api.js         │
  │   request() helper        │
  │   │                       │
  │   │  vite.config.js       │
  │   │  proxy /api → localhost:8000
  │   │                       │
  ▼   ▼                       │
                              │
Django (localhost:8000)        │
  │                           │
  ├─ /api/osimart/cart/*       │
  │   views_osimart.py        │
  │   @csrf_exempt proxy      │
  │   │                       │
  │   └─ OsimartClient ───────┘
  │       services/osimart.py
  │       │
  │       │  HTTPS
  │       ▼
  │   api.osimart.com
  │   /store/apis/cart/*
  │
  └─ /api/cart/*
      views.py
      SessionAuthentication + CSRF
      │
      └─ Django ORM
          Cart / CartItem models
```

**Abstraction layers:**

| Layer | Location | Auth | CSRF |
|-------|----------|------|------|
| Vue composable | `useCart.js` | None (calls API) | None |
| API client | `api.js` | Credentials: same-origin | CSRF token header |
| Django proxy | `views_osimart.py` | Bearer (via OsimartClient) | `@csrf_exempt` |
| Django local | `views.py` | Session | CSRF middleware |
| Osimart external | `api.osimart.com` | Bearer JWT | None |

## 2. Data Models

### 2.1 Django Cart

File: `backend/api/models.py:193-205`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField (PK) | Auto-generated |
| `user` | OneToOneField → User | One cart per user |
| `created_at` | DateTimeField | `auto_now_add=True` |
| `updated_at` | DateTimeField | `auto_now=True` |

### 2.2 Django CartItem

File: `backend/api/models.py:208-238`

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField (PK) | Auto-generated |
| `cart` | ForeignKey → Cart | `related_name="items"`, CASCADE |
| `product` | ForeignKey → Product | `SET_NULL`, nullable (for upgrades/addons) |
| `name` | CharField(200) | Display name |
| `price` | DecimalField(8,2) | Unit price at time of add |
| `quantity` | PositiveIntegerField | Default 1 |
| `image` | CharField(500) | URL, blankable |
| `item_type` | CharField(20) | Choices: product, upgrade, membership, addon |
| `created_at` | DateTimeField | `auto_now_add=True` |

1. Architecture Overview
2. Data Models
3. Frontend Contract (useCart.js)
4. API Client Contract (api.js)
5. Backend Django Views
6. OsimartClient Service
7. External Osimart API
8. Data Flows
9. Migration Path

