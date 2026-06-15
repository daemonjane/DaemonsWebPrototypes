# Contributing

## Setup

```bash
git clone https://github.com/daemonjane/DaemonsWebPrototypes.git
cd DaemonsWebPrototypes/vue-storefront-v2
npm install
npm run dev
```

## Development Workflow

1. Pull latest from both remotes: `git pull origin main && git pull osinode main`
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make changes in `vue-storefront-v2/`
4. Verify build: `cd vue-storefront-v2 && npm run build`
5. Commit using conventional commits: `feat:`, `fix:`, `style:`, `perf:`, `docs:`, `refactor:`, `chore:`
6. Push to both remotes: `git push origin main && git push osinode main`

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add product comparison modal
fix: correct cart total calculation
style: refine hero animation timing
perf: lazy-load product images
docs: update README with new features
refactor: extract filter logic into composable
chore: update Vite config
```

## Build Must Pass

Always run `npm run build` from `vue-storefront-v2/` before committing. The build must exit with 0 errors.

## Project Structure

```
vue-storefront-v2/
├── src/
│   ├── components/     # Reusable Vue components
│   ├── composables/    # Shared state & logic
│   ├── data/           # Product data
│   ├── views/          # Route pages
│   ├── router/         # Route definitions
│   ├── utils/          # Validation helpers
│   ├── App.vue         # Root layout
│   ├── style.css       # Global styles
│   └── main.js         # Entry point
└── public/assets/      # Product images
```

## Code Style

- Vue 3 Composition API with `<script setup>`
- Tailwind CSS for styling
- JSDoc on all composables (see existing for examples)
- Single-file components
- No commented-out code
