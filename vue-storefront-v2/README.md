# TechStore Vue Storefront v2

A Vue 3 SPA storefront for verified high-performance hardware. Built with Vue 3 (Composition API), Vue Router, Tailwind CSS, and Vite.

## Folder Tree

```
vue-storefront-v2/
├── index.html                   # Entry HTML
├── vite.config.js               # Vite + Vue plugin
├── tailwind.config.js           # Custom cyan/slate theme, fonts
├── postcss.config.js            # Tailwind + autoprefixer
├── package.json                 # Dependencies & scripts
├── public/
│   ├── favicon.svg
│   ├── icons.svg
│   └── assets/                  # Product images (SVG placeholders + original fallbacks)
│       ├── stream-deck.svg
│       ├── gaming-chair.svg
│       ├── cpu-cooler.svg
│       ├── nvme-ssd.svg
│       ├── sleeved-cables.svg
│       ├── microphone.svg
│       └── ... (original .jpg/.webp/.png files)
└── src/
    ├── main.js                  # App bootstrap
    ├── App.vue                  # Root: Header + <router-view> + Footer + ToastContainer
    ├── style.css                # Tailwind directives, scrollbar, hero glow, glass header
    ├── router/
    │   └── index.js             # 10 routes (lazy-loaded views)
    ├── data/
    │   └── products.js          # 21 products (15 original + 6 new)
    ├── composables/
    │   ├── useCart.js           # Cart state (localStorage), add/remove/update/clear
    │   ├── useToast.js          # Global toast notifications (auto-dismiss)
    │   ├── useRecentlyViewed.js # Last 6 visited products (localStorage)
    │   └── useFavorites.js      # Wishlist toggle (localStorage)
    ├── utils/
    │   └── validation.js        # isRequired, isValidEmail, validateForm
    ├── components/
    │   ├── Header.vue           # Sticky nav, global search, cart badge, mobile menu
    │   ├── Footer.vue           # Copyright bar
    │   ├── ProductCard.vue      # Reusable card: image, rating, specs, quick-view, favorites, add-to-cart
    │   ├── QuickViewModal.vue   # Teleported modal with focus trap & keyboard support
    │   ├── ImageWithFallback.vue# <img> that shows alt text on error
    │   └── ToastContainer.vue   # Fixed bottom-right toast list
    └── views/
        ├── Home.vue             # Hero, features, recently viewed, featured products, bundles, upgrades, trending, membership, show-more
        ├── Shop.vue             # Filtered/sorted product grid (category, search, sort)
        ├── ProductDetail.vue    # Full product page with specs, favorites, recently-viewed logging
        ├── Favorites.vue        # Wishlist page with clear-all
        ├── Checkout.vue         # Order summary + shipping form with validation
        ├── Login.vue            # Email/password login form
        ├── Register.vue         # Name/email/password registration
        ├── Contact.vue          # Contact form + info
        ├── About.vue            # Static about page
        └── Insights.vue         # Market Pulse dashboard with membership CTA
```

## Data Flow

```
products.js ──► ProductCard ──► QuickViewModal
     │                │
     │                ├── useCart ──► localStorage ──► Checkout
     │                ├── useFavorites ──► localStorage ──► Favorites.vue
     │                └── useRecentlyViewed ──► localStorage ──► Home.vue
     │
     ├── Home.vue (featured, trending, bundles)
     ├── Shop.vue (filtered grid)
     └── ProductDetail.vue (full view)
```

### State Persistence

| Composable | localStorage Key | Data |
|---|---|---|
| `useCart` | `techstore_cart` | Cart items with quantities |
| `useFavorites` | `techstore_favorites` | Array of favorite product IDs |
| `useRecentlyViewed` | `techstore_recently_viewed` | Array of last 6 product IDs |

### Composable Summary

| Composable | Returns | Description |
|---|---|---|
| `useCart()` | `cart`, `totalItems`, `totalPrice`, `addItem()`, `updateQuantity()`, `removeItem()`, `clearCart()`, `addUpgrade()`, `removeUpgrade()`, `setMembership()` | Full cart management with localStorage sync and toast notifications |
| `useToast()` | `toasts`, `addToast(message, duration?)` | Global notification state with auto-dismiss |
| `useRecentlyViewed()` | `items`, `visit(productId)` | Tracks last 6 product visits, persisted |
| `useFavorites()` | `favoriteIds`, `items`, `count`, `toggle(id)`, `isFavorite(id)`, `clear()` | Wishlist management, persisted |

## How to Add a New Page

1. Create `src/views/YourPage.vue` with `<script setup>` + `<template>`
2. Add a lazy import + route in `src/router/index.js`:
   ```js
   const YourPage = () => import('../views/YourPage.vue')
   // In routes array:
   { path: '/your-path', component: YourPage }
   ```
3. Add a nav link in `src/components/Header.vue` (optional)

## How to Add a New Product

1. Add an object to the `products` array in `src/data/products.js`:
   ```js
   {
     id: 'my-product',
     name: 'My Product Name',
     price: 99.99,
     category: 'peripherals', // 'desktop' | 'monitors' | 'peripherals'
     description: 'Short product description.',
     image: '/assets/my-product.svg',
     rating: 4.5,
     specs: ['Spec 1', 'Spec 2', 'Spec 3']
   }
   ```
2. Place an image at `public/assets/my-product.svg` (or .jpg/.webp/.png)
3. The product will automatically appear on the Shop page and become searchable.

## Scripts

```bash
npm run dev      # Start dev server
npm run build    # Production build to dist/
npm run preview  # Preview production build
```

## Styling

- **Tailwind CSS** with custom theme in `tailwind.config.js`
- Colors: cyan (400/500/600/900) + slate (950/900/800/700/600/500/400)
- Fonts: Inter (sans), JetBrains Mono (mono)
- Global styles in `src/style.css`: scrollbar, grid background texture, hero glow, glass header, form validation animations, focus styles

## Accessibility

- Skip-to-content link
- ARIA landmarks (`role="banner"`, `role="region"`, `aria-labelledby`)
- Keyboard navigation with visible focus rings
- Focus trap in QuickViewModal
- Toast notifications use `role="status"` + `aria-live="polite"`
- Semantic heading hierarchy
- Form validation errors linked via `aria-describedby`

## Contribution Guidelines

1. Use Composition API with `<script setup>`
2. Keep views focused — extract reusable UI into `components/`
3. State logic goes in `composables/` with localStorage persistence where appropriate
4. Run `npm run build` before committing
5. Match the existing Tailwind theme — don't add new color palettes
6. Keep product data in `src/data/products.js` — no external API calls
7. Use `ImageWithFallback` for user-uploaded or unreliable image sources
