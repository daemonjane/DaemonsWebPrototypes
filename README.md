<p align="center">
  <img src="https://img.shields.io/badge/Vue_3-4FC08D?logo=vuedotjs&logoColor=white" alt="Vue 3"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white" alt="Vite"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwindcss&logoColor=white" alt="Tailwind CSS"/>
  <img src="https://img.shields.io/badge/Vue_Router-4FC08D?logo=vuedotjs&logoColor=white" alt="Vue Router"/>
  <br/>
  <img src="https://img.shields.io/badge/build-passing-22c55e?logo=checkmarx"/>
  <img src="https://img.shields.io/badge/coverage-21_views-06b6d4"/>
  <img src="https://img.shields.io/badge/license-MIT-blue"/>
</p>

<h1 align="center">🖥️ TechStore — Vue Storefront v2</h1>

<p align="center">
  <b>A production-feature SPA storefront for verified high-performance hardware</b><br/>
  Vue 3 (Composition API) · Vue Router · Tailwind CSS · Vite · SVG
</p>

<br/>

<p align="center">
  <i>Animated particles · Immersive backgrounds · Live notifications · Multi-step checkout · Full legal pages</i>
</p>

<br/>

## 📂 Project Tree

```
📁 vue-storefront-v2/
├── 📄 index.html                   # Entry HTML with font preloads
├── ⚙️ vite.config.js               # Vite + Vue plugin
├── 🎨 tailwind.config.js           # Custom cyan/slate theme, Inter + JetBrains Mono
├── 📦 package.json                 # Dependencies & scripts
├── 📁 public/
│   ├── 🖼️ favicon.svg
│   ├── 🖼️ icons.svg
│   └── 📁 assets/                  # Product images (SVG + original fallbacks)
└── 📁 src/
    ├── 🚀 main.js                  # App bootstrap
    ├── 🏗️ App.vue                  # Root layout + animated background layer
    ├── 🎨 style.css                # Tailwind directives, keyframes, print styles
    ├── 📁 router/
    │   └── 📄 index.js             # 16 lazy-loaded routes
    ├── 📁 data/
    │   └── 📄 products.js          # 21 products across 4 categories
    ├── 📁 composables/             # 🧩 Shared state & logic
    │   ├── 🛒 useCart.js
    │   ├── 🔔 useToast.js
    │   ├── 👁️ useRecentlyViewed.js
    │   ├── ❤️ useFavorites.js
    │   ├── 👥 useLiveVisitorCount.js
    │   ├── 📢 useSalesNotifications.js
    │   ├── 🌓 useTheme.js
    │   ├── ⏳ useRouteLoading.js
    │   └── 📦 useFreeShipping.js
    ├── 📁 utils/
    │   └── 📄 validation.js
    ├── 📁 components/              # 🧱 Reusable UI
    │   ├── 🎨 BackgroundEffects.vue
    │   ├── 🤖 AbstractArt.vue
    │   ├── ⌨️ KeyboardShortcuts.vue
    │   ├── 📋 EmptyState.vue
    │   ├── 🪜 StepperIndicator.vue
    │   ├── 📦 FreeShippingBar.vue
    │   ├── 💀 SkeletonLoader.vue
    │   └── ... (Header, Footer, ProductCard, QuickViewModal, ToastContainer, etc.)
    └── 📁 views/                   # 🖥️ Route pages
        ├── 🏠 Home.vue
        ├── 🛍️ Shop.vue
        ├── 🔍 ProductDetail.vue
        ├── ❤️ Favorites.vue
        ├── 🛒 Checkout.vue
        ├── 🔐 Login.vue
        ├── 📝 Register.vue
        ├── 📞 Contact.vue
        ├── ℹ️ About.vue
        ├── 📊 Insights.vue
        ├── ❓ FAQ.vue
        ├� 📬 OrderTracking.vue
        ├── ✅ OrderConfirmation.vue
        ├── 🔒 PrivacyPolicy.vue
        ├── 📜 TermsOfService.vue
        ├── 🍪 CookiesPolicy.vue
        └� 🚫 NotFound.vue
```

## 🔀 Data Flow

```
products.js ──► ProductCard ──► QuickViewModal
     │                │
     │                ├── useCart ──► localStorage ──► Checkout (multi-step)
     │                ├── useFavorites ──► localStorage ──► Favorites.vue
     │                └── useRecentlyViewed ──► localStorage ──► Home.vue (scroll arrows)
     │
     ├── Home.vue (featured, trends, bundles, testimonials)
     ├── Shop.vue (category filter, search, price sort)
     └── ProductDetail.vue (zoom, stock badges, share, back-in-stock)
```

## 🗄️ State Persistence

| Composable | localStorage Key | Stores |
|-----------|-----------------|--------|
| `useCart` | `techstore_cart` | Cart items, quantities, upgrades, membership |
| `useFavorites` | `techstore_favorites` | Array of favorite product IDs |
| `useRecentlyViewed` | `techstore_recently_viewed` | Last 6 visited product IDs |
| `useTheme` | `techstore_theme` | `'dark'` or `'light'` |
| `useLiveVisitorCount` | `techstore_visitor_count` | Fluctuating visitor counter |
| `CookiesPolicy` | `cookie_preferences` | JSON with essential/analytics/marketing booleans |

## 🧩 Composable API

| Composable | Returns |
|-----------|---------|
| `useCart()` | `cart`, `totalItems`, `totalPrice`, `addItem()`, `updateQuantity()`, `removeItem()`, `clearCart()`, `addUpgrade()`, `removeUpgrade()`, `setMembership()` |
| `useToast()` | `toasts`, `addToast(message, type?)` |
| `useRecentlyViewed()` | `items`, `visit(productId)` |
| `useFavorites()` | `favoriteIds`, `items`, `count`, `toggle(id)`, `isFavorite(id)`, `clear()` |
| `useTheme()` | `isDark`, `toggle()` |
| `useRouteLoading()` | `showSkeleton`, `startLoading()` |
| `useLiveVisitorCount()` | `count` (ref) |
| `useSalesNotifications()` | — (calls `useToast()` internally) |
| `useFreeShipping()` | `remaining`, `progress`, `qualifies`, `threshold` |

## 📦 Scripts

```bash
npm run dev       # Start Vite dev server
npm run build     # Production build → dist/
npm run preview   # Preview production build
```

## 🎨 Styling

- **Tailwind CSS** with custom cyan/slate theme
- **Fonts:** Inter (sans), JetBrains Mono (mono)
- **Global styles:** Scrollbar, grid background texture, hero glow, glass header, form validation animations, keyframes for particles/orbs, print styles, dark/light theme overrides
- **Dark mode:** Class-based with smooth CSS transitions

## ♿ Accessibility

- Skip-to-content link
- ARIA landmarks (`role="banner"`, `role="region"`, `aria-labelledby`)
- Keyboard navigation with visible focus rings (`focus-visible`)
- Focus trap in QuickViewModal
- Toast notifications use `role="status"` + `aria-live="polite"`
- Semantic heading hierarchy
- Form validation errors linked via `aria-describedby`

## 📝 How to Add a Page

1. Create `src/views/YourPage.vue`
2. Add lazy import + route in `src/router/index.js`:
   ```js
   const YourPage = () => import('../views/YourPage.vue')
   { path: '/your-path', component: YourPage }
   ```
3. Add nav link in `src/components/Header.vue` (optional)

## 📝 How to Add a Product

1. Add to `src/data/products.js`:
   ```js
   {
     id: 'my-product',
     name: 'My Product Name',
     price: 99.99,
     category: 'peripherals',   // 'desktop' | 'monitors' | 'peripherals'
     description: '...',
     image: '/assets/my-product.svg',
     rating: 4.5,
     specs: ['Spec 1', 'Spec 2'],
     stock: 15
   }
   ```
2. Place image at `public/assets/my-product.*`
3. Appears automatically on Shop + becomes searchable.

## 🤝 Contribution

1. Use Composition API with `<script setup>`
2. Views → page logic; Components → reusable UI; Composables → state
3. Run `npm run build` before committing
4. Match existing Tailwind theme — no new color palettes
5. Product data in `src/data/products.js` — no external API calls
