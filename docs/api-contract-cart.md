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

### 2.3 DRF Serializers

File: `backend/api/serializers.py:8-37`

**CartItemSerializer** fields: `id`, `product_slug` (readOnly, from FK), `product_image` (method field → falls back to item.image then product.image), `name`, `price`, `quantity`, `image`, `item_type`, `created_at`.

**CartSerializer** fields: `id`, `items` (nested CartItemSerializer, many, readOnly), `total_price` (method field → sum of price*qty), `total_items` (method field → sum of qty), `created_at`, `updated_at`.

Example serialized cart response:

```json
{
  "id": 1,
  "items": [
    {
      "id": 10,
      "product_slug": "gaming-mouse",
      "product_image": "https://...",
      "name": "Gaming Mouse",
      "price": "49.99",
      "quantity": 2,
      "image": "",
      "item_type": "product",
      "created_at": "2026-07-03T10:00:00Z"
    }
  ],
  "total_price": 99.98,
  "total_items": 2,
  "created_at": "2026-07-03T10:00:00Z",
  "updated_at": "2026-07-03T10:00:00Z"
}
```

### 2.4 Osimart External Cart Response Shape

Returned by `GET /store/apis/cart/view/` (via `OsimartClient.get_cart()`).

```json
{
  "cart": {
    "<variant-uuid>": {
      "id": "<variant-uuid>",
      "item_id": "<variant-uuid>",
      "name": "Gaming Mouse",
      "price": "49.99",
      "unit_price": "49.99",
      "quantity": 2,
      "image": "static/images/uploaded_files/gaming-mouse.jpg",
      "product_image": "static/images/uploaded_files/gaming-mouse.jpg",
      "item_type": "product",
      "product_id": "<product-uuid>"
    }
  },
  "total_price": "99.98",
  "total_items": 3,
  "total_quantity": 3
}
```

Key differences from Django serialized cart:
- `cart` is an **object** keyed by variant UUID, not an array
- Prices are **strings**, not numbers
- Item IDs are **ProductVariant UUIDs**, not auto-increment integers
- Images are **relative paths**, not full URLs
- `product_id` is separate from the item key

## 3. Frontend Contract (useCart.js)

File: `src/composables/useCart.js`

### 3.1 Exported Functions

| Function | Parameters | Returns | API Call | Description |
|----------|-----------|---------|----------|-------------|
| `init()` | none | `Promise<void>` | GET `/api/osimart/cart/view/` | Check user login, fetch server cart, set mode |
| `refresh()` | none | `Promise<void>` | GET `/api/osimart/cart/view/` | Re-fetch server cart (no-op if local mode) |
| `addItem(product, quantity=1)` | `product: Object`, `quantity: Number` | `Promise<void>` | POST `/api/osimart/cart/update-item/` | Add item with `action:'add'` or push to local |
| `updateQuantity(productId, delta)` | `productId: String`, `delta: Number` | `Promise<void>` | POST `/api/osimart/cart/update-item/` | Increment/decrement; remove if <=0 |
| `removeItem(productId)` | `productId: String` | `Promise<void>` | POST `/api/osimart/cart/update-item/` | Remove item with `action:'remove_all'` |
| `clearCart()` | none | `Promise<void>` | POST per item + GET refresh | Remove all items one by one |
| `addUpgrade(id, name, price)` | `id, name, price` | `Promise<void>` | Delegates to `addItem` | Wraps upgrade as product with `type:'upgrade'` |
| `removeUpgrade(id, name)` | `id, name` | `Promise<void>` | Delegates to `removeItem` | Removes upgrade item |
| `setMembership(type, name, price)` | `type: String|null`, `name, price` | `Promise<void>` | POST per removal + POST add | Replace all memberships with new one |
| `mergeLocalIntoServer()` | none | `Promise<void>` | POST per local item + GET refresh | Upload local cart to osimart, clear local |

### 3.2 Computed Properties

| Property | Type | Server Mode | Local Mode |
|----------|------|-------------|------------|
| `cart` | `Array<Object>` | `Object.values(serverCart.value.cart).map(osimartItemToLocal)` | `localCart.value` |
| `totalItems` | `Number` | Sum of `quantity` from server cart object, fallback `total_items`/`total_quantity` | `reduce` sum of `quantity` |
| `totalPrice` | `Number` | `parseFloat(serverCart.value.total_price \|\| serverCart.value.total \|\| 0)` | `reduce` sum of `price * quantity` |

### 3.3 Module-level Helper: `osimartItemToLocal(item)`

File: `src/composables/useCart.js:16-26`

Maps osimart API response item → local cart shape:

| Local Field | Source |
|------------|--------|
| `id` | `item.item_id \|\| item.product_id \|\| item.id \|\| \`item-${Date.now()}\`` |
| `_serverId` | `item.id` (raw osimart key) |
| `name` | `item.name \|\| item.product_name \|\| ''` |
| `price` | `parseFloat(item.price \|\| item.unit_price \|\| 0)` |
| `quantity` | `item.quantity \|\| 1` |
| `image` | `resolveImage(item.image) \|\| resolveImage(item.product_image) \|\| ''` |
| `type` | `item.item_type \|\| item.type \|\| 'product'` |

`resolveImage()` prepends `https://api.osimart.com/` to relative paths.

### 3.4 Module State

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `localCart` | `ref<Array>` | `localStorage['techstore_cart']` or `[]` | Local cart items, persisted to localStorage on change |
| `serverCart` | `ref<Object\|null>` | `null` | Raw osimart cart response |
| `useServer` | `Boolean` | `false` | Whether to use osimart server (true) or localStorage (false) |

## 4. API Client Contract (api.js)

File: `src/utils/api.js`

### 4.1 `request()` Helper (lines 9-26)

| Property | Value |
|----------|-------|
| Signature | `async function request(method, path, body?)` |
| CSRF | Adds `X-CSRFToken` for POST/PUT/PATCH/DELETE |
| Auth | `credentials: 'same-origin'` (session cookie) |
| Content-Type | `application/json` |
| Error | Parses JSON error body, throws `Error(data.error)` |
| Base | `''` (proxied by Vite → Django) |

### 4.2 `api.osimartCart` (lines 35-38)

| Method | Signature | HTTP | Path |
|--------|-----------|------|------|
| `view()` | `() => request('GET', ...)` | GET | `/api/osimart/cart/view/` |
| `updateItem(data)` | `(data) => request('POST', ...)` | POST | `/api/osimart/cart/update-item/` |

### 4.3 `api.cart` — Legacy Local (lines 46-53)

| Method | Signature | HTTP | Path |
|--------|-----------|------|------|
| `get()` | `() => request('GET', ...)` | GET | `/api/cart/` |
| `add(data)` | `(data) => request('POST', ...)` | POST | `/api/cart/add/` |
| `updateItem(itemId, data)` | `(itemId, data) => request('PATCH', ...)` | PATCH | `/api/cart/item/${itemId}/` |
| `removeItem(itemId)` | `(itemId) => request('DELETE', ...)` | DELETE | `/api/cart/item/${itemId}/` |
| `clear()` | `() => request('POST', ...)` | POST | `/api/cart/clear/` |
| `merge(items)` | `(items) => request('POST', ...)` | POST | `/api/cart/merge/` |

### 4.4 CSRF

- `getCSRFToken()` reads `csrftoken` cookie
- `ensureCSRF()` calls GET `/api/auth/csrf/` if missing (main.js startup)
- Unsafe methods send `X-CSRFToken` header
- Osimart proxy views (`/api/osimart/cart/*`) use `@csrf_exempt` → CSRF not needed

## 5. Backend Django Views

File: `backend/api/views.py` (local), `backend/api/views_osimart.py` (proxy)

### 5.1 Local Cart Views — Overview

| URL | Method | View Function | Auth | CSRF | File:Line |
|-----|--------|---------------|------|------|-----------|
| `/api/cart/` | GET | `cart_get` | Session required | Yes | `views.py:163` |
| `/api/cart/add/` | POST | `cart_add` | Session required | Yes | `views.py:170` |
| `/api/cart/item/<int:id>/` | PATCH | `cart_item_detail` | Session required | Yes | `views.py:207` |
| `/api/cart/item/<int:id>/` | DELETE | `cart_item_detail` | Session required | Yes | `views.py:207` |
| `/api/cart/clear/` | POST | `cart_clear` | Session required | Yes | `views.py:237` |
| `/api/cart/merge/` | POST | `cart_merge` | Session required | Yes | `views.py:247` |

### 5.2 `cart_get` — GET `/api/cart/`

| Property | Value |
|----------|-------|
| Decorators | `@api_view(['GET'])` |
| Auth | `request.user.is_authenticated` → 401 |
| Logic | `_get_cart(user)` → `CartSerializer` |
| Response | Full cart JSON with items array, totals |
| Error | `{"error": "Not authenticated."}` (401) |

### 5.3 `cart_add` — POST `/api/cart/add/`

| Property | Value |
|----------|-------|
| Decorators | `@api_view(['POST'])` |
| Auth | `request.user.is_authenticated` → 401 |
| Body | `{item_type? (default "product"), name, price, quantity? (default 1), image?}` |
| Logic | If same `item_type`+`name` exists: increment qty. Addon duplicates return 409. Else create new `CartItem`. |
| Response | Full cart JSON |
| Errors | `{"error": "Not authenticated."}` (401), `{"error": "Add-on already in cart."}` (409) |

### 5.4 `cart_item_detail` — PATCH/DELETE `/api/cart/item/<int:id>/`

| Property | Value |
|----------|-------|
| Decorators | `@api_view(['PATCH', 'DELETE'])` |
| Auth | `request.user.is_authenticated` → 401 |
| PATCH Body | `{quantity?, price?, name?}` — quantity clamped at 0 |
| PATCH Logic | Update fields. If quantity ≤ 0 → delete item. |
| DELETE | Removes item, returns full cart |
| Response | Full cart JSON |
| Errors | `{"error": "Not authenticated."}` (401), `{"error": "Item not found."}` (404) |

### 5.5 `cart_clear` — POST `/api/cart/clear/`

| Property | Value |
|----------|-------|
| Decorators | `@api_view(['POST'])` |
| Auth | `request.user.is_authenticated` → 401 |
| Logic | `cart.items.all().delete()` |
| Response | Full cart JSON (empty items array) |

### 5.6 `cart_merge` — POST `/api/cart/merge/`

| Property | Value |
|----------|-------|
| Decorators | `@api_view(['POST'])` |
| Auth | `request.user.is_authenticated` → 401 |
| Body | `{items: [{item_type, name, price, quantity, image}]}` |
| Logic | For each item: if exists with same `item_type`+`name` → increment qty, else create new `CartItem` |
| Response | Full cart JSON |

### 5.7 Helper Functions

| Function | Location | Purpose |
|----------|----------|---------|
| `_get_cart(user)` | `views.py:152` | `Cart.objects.get_or_create(user=user)` |
| `_cart_json(cart)` | `views.py:157` | Re-fetches cart from DB, serializes via `CartSerializer` |

### 5.8 Osimart Proxy Views — Overview

| URL | Method | View Function | Auth | CSRF | File:Line |
|-----|--------|---------------|------|------|-----------|
| `/api/osimart/cart/view/` | GET | `osimart_cart_view` | None (proxied) | `@csrf_exempt` | `views_osimart.py:254` |
| `/api/osimart/cart/update-item/` | POST | `osimart_cart_update_item` | None (proxied) | `@csrf_exempt` | `views_osimart.py:265` |

### 5.9 `osimart_cart_view` — GET `/api/osimart/cart/view/`

| Property | Value |
|----------|-------|
| Decorators | `@require_GET`, `@csrf_exempt` |
| Logic | `client = _get_client()` → `data = client.get_cart()` → `JsonResponse(data)` |
| Response | Raw osimart API response (object cart format) |

### 5.10 `osimart_cart_update_item` — POST `/api/osimart/cart/update-item/`

| Property | Value |
|----------|-------|
| Decorators | `@require_POST`, `@csrf_exempt` |
| Body | `{item_id, action, quantity?, name?, price?, image?, item_type?, store?}` |
| Logic | Parses `item_id` + `action` from body, calls `client.update_cart_item(item_id, action, body)` |
| Response | Raw osimart API response |

## 6. OsimartClient Service

File: `backend/services/osimart.py`

### 6.1 Class Overview

| Property | Value |
|----------|-------|
| Class | `OsimartClient` |
| BASE_URL | `os.environ.get("OSIMART_API_BASE_URL", "https://api.osimart.com")` |
| STORE_ID | `os.environ.get("OSIMART_STORE_ID", "")` |
| Auth | JWT Bearer token from `POST /auth/login/` with email+password |
| Token Lifetime | 30 min default; auto-refresh on 401 via `_refresh()` or re-login |

### 6.2 Auth Flow

| Method | Lines | Purpose |
|--------|-------|---------|
| `_login()` | 37-52 | `POST {BASE_URL}/auth/login/` with `OSIMART_EMAIL`/`OSIMART_PASSWORD` → stores access_token |
| `_refresh()` | 54-60 | `POST {BASE_URL}/auth/token/refresh/` with stored refresh_token |
| `_ensure_token()` | 30-35 | Checks if token expired; calls `_refresh()` or `_login()` |
| `_get_headers()` | 65-70 | Calls `_ensure_token()` → returns `Authorization: Bearer {token}` + Content-Type |

### 6.3 `get_cart()` — GET `/store/apis/cart/view`

| Property | Value |
|----------|-------|
| Lines | 152-163 |
| URL | `{BASE_URL}/store/apis/cart/view` |
| Method | GET |
| Params | `?store={STORE_ID}` appended |
| 401 Retry | Clears token, retries once |
| Error | Raises `OsimartError` on failure |
| Response | Raw JSON (object cart format) |

### 6.4 `update_cart_item()` — POST `/store/apis/cart/update-item/`

| Property | Value |
|----------|-------|
| Lines | 166-180 |
| URL | `{BASE_URL}/store/apis/cart/update-item/` |
| Method | POST |
| Payload | `{store: STORE_ID, item_id, action, ...data}` |
| Fields | `item_id` (required), `action` (required: `add`/`remove`/`remove_all`), rest forwarded from `data` |
| 401 Retry | Clears token, retries once |
| Error | Raises `OsimartError` on failure |
| Response | Raw JSON (updated cart) |

### 6.5 URL Base Divergence

| Helper | Base Path | Used For |
|--------|-----------|----------|
| `_store_api_url(path)` | `{BASE_URL}/store/apis/{path}` | Cart only |
| `_api_url(path)` | `{BASE_URL}/dashboard/apis/{path}` | All other resources (products, banners, categories, etc.) |

This divergence is critical: cart endpoints live under `/store/apis/` while everything else lives under `/dashboard/apis/`.

## 7. External Osimart API

### 7.1 `GET /store/apis/cart/view`

| Property | Value |
|----------|-------|
| Host | `https://api.osimart.com` |
| Path | `/store/apis/cart/view` |
| Method | GET |
| Query | `?store={store_id}` |
| Auth | `Authorization: Bearer {jwt}` |
| Response | `{cart: {<uuid>: {...}}, total_price, total_items, total_quantity}` |

### 7.2 `POST /store/apis/cart/update-item/`

| Property | Value |
|----------|-------|
| Host | `https://api.osimart.com` |
| Path | `/store/apis/cart/update-item/` |
| Method | POST |
| Body | `{store, item_id, action, quantity?, name?, price?, image?, item_type?}` |
| Auth | `Authorization: Bearer {jwt}` |
| Actions | `add` (set qty), `remove` (requires qty param), `remove_all` (no param) |
| Response | Updated cart object

