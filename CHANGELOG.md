# Changelog

## [Unreleased]

### Added
- Project-root README with monorepo overview and remotes
- Privacy Policy, Terms of Service, and Cookies Policy pages with interactive controls
- Enhanced About page with animated counters, expandable value cards, collapsible timeline
- Footer links to legal pages
- Order tracking page with timeline visualization
- Multi-step checkout (Shipping → Payment → Review) with stepper indicator
- Gift card balance checker with discount application
- Share product button (Web Share API + clipboard fallback)
- EmptyState component with 4 icon variants
- Live visitor count with animated dot in footer
- Sales notification popup every 30 seconds
- Print-friendly CSS styles
- SkeletonLoader detail variant on ProductDetail
- `v-memo` optimization on product card lists
- Native `loading="lazy"` on all product images
- Google Fonts preload links
- Dark/light theme toggle with localStorage persistence
- Back-in-stock notification form on out-of-stock products
- Stock status badges (red/amber/green) on ProductDetail
- Animated counter component for Home metrics
- Toasts with success/error/default types
- Recently viewed products strip on Home
- Favorites/wishlist with dedicated page
- Quick View modal with focus trap
- Page transition animations
- 404 page with glitch effect
- Scroll-to-top button
- Breadcrumb navigation on Shop and ProductDetail
- Product badges (NEW, BEST SELLER, PREMIUM)
- FAQ accordion page
- Testimonials section on Home
- Price range slider on Shop
- Sticky mobile add-to-cart bar
- 6 new products with SVG placeholder images

### Fixed
- Header.vue rewritten as proper navigation (was a copy of Home.vue)
- ProductDetail.vue missing closing `</div>` on image wrapper
- Theme flash prevented by setting dark class before Vue mounts
- Contact form validation ref binding

### Changed
- Shop filter buttons show product counts
- Upgraded checkout from single form to 3-step flow
- Footer redesigned with nav columns, social icons, newsletter
