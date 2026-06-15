# DaemonsWebPrototypes

A monorepo of web prototypes and storefront experiments by Daemon.

## Projects

### [vue-storefront-v2](./vue-storefront-v2/README.md)

A production-feature Vue 3 storefront — rebuilt from scratch with enhanced visuals, composable architecture, and full-page transitions.

**Stack:** Vue 3 (Composition API) · Vite · Tailwind CSS · Vue Router · SVG

**Features:**
- Product catalogue with 21 items across 4 categories
- Global search with grouped live dropdown results by category
- Cart with upgrades, membership tiers, and bundle support
- Favorites / Wishlist with localStorage persistence
- Recently viewed products with scroll arrows
- Quick View modal with focus trap and keyboard support
- Multi-step checkout (Shipping → Payment → Review) with floating form labels
- Gift card balance checker with 10% mock discount
- Order tracking page with animated timeline
- Order confirmation page with order number
- Dark / Light theme toggle with smooth CSS transitions
- Skeleton loaders for lazy-loaded routes
- Animated counters, live visitor count, sales notifications
- Immersive animated background (particles, glow orbs, noise texture)
- AI-generated abstract geometric SVG art on Home hero and About page
- Stock level dots indicator on product cards
- Price comparison tooltip (below/above category average)
- Category hero banners with emoji icons
- Free shipping progress bar
- Loading spinner buttons for add-to-cart
- Keyboard shortcut modal (press `?`)
- Enhanced 404 page with animated radar SVG
- Image zoom on ProductDetail hover
- Animated tech stack bars on About page
- Legal pages: Privacy Policy, Terms of Service, Cookies Policy (interactive)
- Print-friendly CSS styles
- Fully responsive with mobile hamburger menu and sticky add-to-cart bar

## Getting Started

```bash
# Install dependencies
cd vue-storefront-v2 && npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

## Commit Convention

This repo uses [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `style:` — styling / CSS
- `perf:` — performance improvement
- `docs:` — documentation
- `refactor:` — code restructuring
- `chore:` — tooling / config

## Branch

The current v2 storefront lives on `frontend-vue-final-version`. This branch contains all features, fixes, and documentation for the latest build.

```bash
git checkout frontend-vue-final-version
```

## Remotes

| Remote | URL |
|--------|-----|
| `origin` | github.com/daemonjane/DaemonsWebPrototypes |
| `osinode` | git.osinode.com/Ositcom/charbel_elias |
