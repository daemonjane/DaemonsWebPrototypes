# DaemonsWebPrototypes

A monorepo of web prototypes and storefront experiments by Daemon.

## Projects

### [vue-storefront-v2](./vue-storefront-v2/README.md)

A production-feature Vue 3 storefront — rebuilt from scratch with enhanced visuals, composable architecture, and full-page transitions.

**Stack:** Vue 3 (Composition API) · Vite · Tailwind CSS · Vue Router

**Features:**
- Product catalogue with 21 items across 4 categories
- Global search with live dropdown results
- Cart with upgrades, membership tiers, and bundle support
- Favorites / Wishlist with localStorage persistence
- Recently viewed products tracker
- Quick View modal with focus trap and keyboard support
- Multi-step checkout with gift card checker
- Order tracking page with timeline
- Dark / Light theme toggle
- Skeleton loaders for lazy-loaded routes
- Animated counters, live visitor count, sales notifications
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

## Remotes

| Remote | URL |
|--------|-----|
| `origin` | github.com/daemonjane/DaemonsWebPrototypes |
| `osinode` | git.osinode.com/Ositcom/charbel_elias |
