
# TechStore Frontend – Complete E‑commerce Store

[![GitHub release](https://img.shields.io/badge/version-v1.0-blue)](https://github.com/daemonjane/DaemonsWebPrototypes/releases/tag/v1.0)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4.17-38B2AC)](https://tailwindcss.com/)

A fully responsive, multi‑page tech store built with vanilla HTML, Tailwind CSS, and JavaScript. Designed to be easily connected to a backend API. Features include dynamic product listing, persistent cart, user authentication mock, and a design system shared across all pages.

## 📁 Project Structure
techstore-full/
├── index.html # Homepage (hero, features, bundles, upgrades, insights)
├── shop.html # Product listing with filtering, sorting, search
├── product-detail.html # Individual product view (dynamic via URL param)
├── checkout.html # Order summary and shipping form
├── login.html / register.html # Mock authentication
├── about.html / contact.html / insights.html
├── assets/ # Product images and icons
├── src/
│ └── input.css # Tailwind source + custom global styles
├── dist/
│ └── output.css # Minified Tailwind build
├── tailwind.config.js # Custom colors, fonts, animations
├── package.json # Dependencies (Tailwind only)
└── README.md


## 🚀 Features

- **Responsive design** – works on mobile, tablet, desktop.
- **Dynamic product catalog** – filter by category, sort by price/name, live search.
- **Cart with quantity** – add/remove items, adjust quantities, persistent via `localStorage`.
- **Product detail pages** – dynamic content based on URL parameter.
- **Toast notifications** – user feedback when adding items.
- **Shared design system** – consistent header, footer, buttons, scrollbar, grid background.
- **Mock authentication** – login/register stores user in `localStorage`.
- **Modular JavaScript** – cart logic reused across all pages.

## 🛠️ Setup & Development

### Prerequisites
- Node.js (for Tailwind CSS building)
- Any static web server (Python, nginx, etc.)

### Install dependencies
```bash
npm install


## 🔄 Git Workflow (Version Control Strategy)

This repository follows a **Git Flow** inspired branching model:

- `main` – production-ready code. Every commit on `main` is tagged with a version number (e.g., `v1.0.0`).
- `develop` – integration branch for features. All feature branches are merged here first.
- `staging` – pre‑release testing. Merged from `develop` before going to `main`.
- `feature/*` – individual features or bug fixes. Created from `develop` and merged back via pull requests.

### Workflow Steps

1. **Create a feature branch** from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name




