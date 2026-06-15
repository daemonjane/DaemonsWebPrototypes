<p align="center">
  <img src="https://img.shields.io/badge/Vue_3-4FC08D?logo=vuedotjs&logoColor=white" alt="Vue 3"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white" alt="Vite"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwindcss&logoColor=white" alt="Tailwind CSS"/>
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License"/>
  <br/>
  <img src="https://img.shields.io/github/last-commit/daemonjane/DaemonsWebPrototypes?color=06b6d4&logo=github"/>
  <img src="https://img.shields.io/github/repo-size/daemonjane/DaemonsWebPrototypes?color=a78bfa&logo=files"/>
</p>

<h1 align="center">⚡ DaemonsWebPrototypes ⚡</h1>

<p align="center">
  <b>Monorepo of web prototypes & storefront experiments</b><br/>
  Built with Vue 3 · Vite · Tailwind CSS · Vue Router · SVG
</p>

<br/>

## 📦 Projects

### [🚀 vue-storefront-v2](./vue-storefront-v2/README.md)

A production-feature Vue 3 storefront — rebuilt from scratch with an immersive UI, composable architecture, animated backgrounds, and full-page transitions.

| Area | Highlights |
|------|-----------|
| **Catalogue** | 21 products across 4 categories, grouped search, category banners |
| **Cart** | Multi-step checkout (Shipping→Payment→Review), gift card 10% discount, upgrades, memberships |
| **UX** | Dark/light theme transition, keyboard shortcuts (`?`), skeleton loaders, floating labels |
| **Visuals** | Animated particles + glow orbs + noise texture background, AI-generated SVG art, zoom effects |
| **Pages** | Shop, ProductDetail, Favorites, Order Tracking, Order Confirmation, 404, Legal (Privacy/Terms/Cookies) |
| **Composables** | `useCart`, `useFavorites`, `useRecentlyViewed`, `useToast`, `useLiveVisitorCount`, `useSalesNotifications`, `useFreeShipping` |

<details>
<summary><b>🌟 Full Feature List</b></summary>

<br/>

| # | Feature | Status |
|---|---------|--------|
| 1 | 📦 Product catalogue with 21 items across 4 categories | ✅ |
| 2 | 🔍 Global search with grouped live dropdown results by category | ✅ |
| 3 | 🛒 Cart with upgrades, membership tiers, and bundle support | ✅ |
| 4 | ❤️ Favorites / Wishlist with localStorage persistence | ✅ |
| 5 | 👁️ Recently viewed products with scroll arrows | ✅ |
| 6 | 🔎 Quick View modal with focus trap and keyboard support | ✅ |
| 7 | 🚚 Multi-step checkout (Shipping → Payment → Review) with floating form labels | ✅ |
| 8 | 🎁 Gift card balance checker with 10% mock discount | ✅ |
| 9 | 📬 Order tracking page with animated timeline | ✅ |
| 10 | ✅ Order confirmation page with order number | ✅ |
| 11 | 🌓 Dark / Light theme toggle with smooth CSS transitions | ✅ |
| 12 | 💀 Skeleton loaders for lazy-loaded routes | ✅ |
| 13 | 📊 Animated counters, live visitor count, sales notifications | ✅ |
| 14 | 🎨 Immersive animated background (particles, glow orbs, noise texture) | ✅ |
| 15 | 🤖 AI-generated abstract geometric SVG art on Home hero and About page | ✅ |
| 16 | 🔴 Stock level dots indicator on product cards | ✅ |
| 17 | 💲 Price comparison tooltip (below/above category average) | ✅ |
| 18 | 🏷️ Category hero banners with emoji icons | ✅ |
| 19 | 📦 Free shipping progress bar | ✅ |
| 20 | ⏳ Loading spinner buttons for add-to-cart | ✅ |
| 21 | ⌨️ Keyboard shortcut modal (press `?`) | ✅ |
| 22 | 🚀 Enhanced 404 page with animated radar SVG | ✅ |
| 23 | 🔍 Image zoom on ProductDetail hover | ✅ |
| 24 | 📈 Animated tech stack bars on About page | ✅ |
| 25 | ⚖️ Legal pages: Privacy Policy, Terms of Service, Cookies Policy (interactive) | ✅ |
| 26 | 🖨️ Print-friendly CSS styles | ✅ |
| 27 | 📱 Fully responsive with mobile hamburger menu and sticky add-to-cart bar | ✅ |
</details>

<br/>

## 🚀 Getting Started

```bash
cd vue-storefront-v2 && npm install
npm run dev      # → http://localhost:5173
npm run build    # → dist/
```

## 🌿 Branch

```bash
git checkout frontend-vue-final-version
```

All current v2 work lives on `frontend-vue-final-version` — includes all features, fixes, and docs.

## 📝 Commit Convention

| Type | Usage |
|------|-------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `style:` | Styling / CSS |
| `perf:` | Performance improvement |
| `docs:` | Documentation |
| `refactor:` | Code restructuring |
| `chore:` | Tooling / config |

## 🌐 Remotes

| Remote | URL |
|--------|-----|
| `origin` | [github.com/daemonjane/DaemonsWebPrototypes](https://github.com/daemonjane/DaemonsWebPrototypes) |
| `osinode` | [git.osinode.com/Ositcom/charbel_elias](https://git.osinode.com/Ositcom/charbel_elias) |
