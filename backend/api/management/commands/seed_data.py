from django.core.management.base import BaseCommand

from api.models import Category, Product, ProductAddon


PRODUCTS = [
    {
        "slug": "vanguard-desktop",
        "name": "Vanguard Series i7 / RTX 5070",
        "price": "2499.00",
        "category": "desktop",
        "description": "Liquid-cooled extreme desktop. Ultimate performance.",
        "image": "/assets/vanguard-desktop-fallback.png",
        "rating": 4.8,
        "specs": ["RTX 5070 12GB", "Intel i7-14th 20-Core", "32GB DDR5", "360mm AIO"],
        "stock": 5,
    },
    {
        "slug": "ultrawide-monitor",
        "name": '34" QD-OLED Ultrawide',
        "price": "899.00",
        "category": "monitors",
        "description": "240Hz, 0.03ms, infinite contrast. Perfect for immersion.",
        "image": "/assets/ultrawide-monitor-fallback.png",
        "rating": 4.9,
        "specs": ["QD-OLED Panel", "3440x1440", "240Hz Refresh", "0.03ms Response"],
        "stock": 0,
    },
    {
        "slug": "cyberpro-keyboard",
        "name": "Cyber-Pro Mechanical Keyboard",
        "price": "129.00",
        "category": "peripherals",
        "description": "Hot-swappable brown switches, RGB, aluminum frame.",
        "image": "/assets/cyberpro-keyboard-fallback.png",
        "rating": 4.5,
        "specs": ["Tactile Brown Switches", "Aerospace Aluminum", "USB-C / 2.4GHz", "RGB per-key"],
    },
    {
        "slug": "gaming-mouse",
        "name": "Precision Gaming Mouse",
        "price": "79.99",
        "category": "peripherals",
        "description": "16K DPI, 6 programmable buttons, lightweight.",
        "image": "/assets/gamingmouse.jpg",
        "rating": 4.6,
        "specs": ["16,000 DPI", "6 Buttons", "69g Weight", "RGB Lighting"],
    },
    {
        "slug": "wireless-headset",
        "name": "Wireless ANC Headset",
        "price": "149.99",
        "category": "peripherals",
        "description": "Low-latency 2.4GHz + Bluetooth 5.3, 40h battery.",
        "image": "/assets/headset.jpg",
        "rating": 4.7,
        "specs": ["Active Noise Cancelling", "40h Battery", "Low-latency Wireless", "Retractable Mic"],
    },
    {
        "slug": "usb-hub",
        "name": "Powered USB-C Hub (7-Port)",
        "price": "59.99",
        "category": "peripherals",
        "description": "10Gbps transfer, 60W PD pass-through.",
        "image": "/assets/USBhub.jpg",
        "rating": 4.4,
        "specs": ["7 x USB 3.2", "60W Power Delivery", "10Gbps Speed", "Individual Switches"],
    },
    {
        "slug": "mousepad",
        "name": "RGB Extended Mouse Mat",
        "price": "34.99",
        "category": "peripherals",
        "description": "900x400mm spill-proof surface with 12 lighting zones.",
        "image": "/assets/mousepad.jpg",
        "rating": 4.3,
        "specs": ["900x400mm", "Spill-proof", "12 RGB Zones", "Non-slip Base"],
    },
    {
        "slug": "webcam",
        "name": "4K Streaming Webcam",
        "price": "99.99",
        "category": "peripherals",
        "description": "Auto-framing, built-in ring light, privacy shutter.",
        "image": "/assets/webcam.webp",
        "rating": 4.5,
        "specs": ["4K 30fps", "Auto-framing", "Ring Light", "Privacy Shutter"],
    },
    {
        "slug": "speakers",
        "name": "2.1 Desktop Speaker System",
        "price": "129.99",
        "category": "peripherals",
        "description": "80W RMS, Bluetooth 5.0, wooden subwoofer.",
        "image": "/assets/speakers.jpg",
        "rating": 4.4,
        "specs": ["80W RMS", "Bluetooth 5.0", "Wooden Sub", "Wired & Wireless"],
    },
    {
        "slug": "thermal-paste",
        "name": "Thermal Matrix Pro Paste",
        "price": "6.99",
        "category": "peripherals",
        "description": "High-performance thermal compound.",
        "image": "/assets/ThermalCompound2.jpg",
        "rating": 4.7,
        "specs": ["4g Syringe", "Non-conductive", "Stable up to 350°C"],
    },
    {
        "slug": "cable-ties",
        "name": "Braided Cable Ties (10pk)",
        "price": "4.50",
        "category": "peripherals",
        "description": "Magnetic cable management.",
        "image": "/assets/BraidedCableTies.jpg",
        "rating": 4.2,
        "specs": ["10-pack", "Braided", "Magnetic"],
    },
    {
        "slug": "cleaning-kit",
        "name": "Anti-Static Cleaning Kit",
        "price": "8.99",
        "category": "peripherals",
        "description": "Microfiber + solution for screens and components.",
        "image": "/assets/CleaningKit.jpg",
        "rating": 4.5,
        "specs": ["Microfiber Cloth", "Cleaning Solution", "Anti-static"],
    },
    {
        "slug": "gpu-bracket",
        "name": "GPU Support Bracket",
        "price": "12.99",
        "category": "peripherals",
        "description": "Adjustable support for heavy graphics cards.",
        "image": "/assets/GPU_support_bracket.jpg",
        "rating": 4.3,
        "specs": ["Adjustable Height", "Magnetic Base", "Rubber Padding"],
    },
    {
        "slug": "displayport-cable",
        "name": "DisplayPort 2.1 Cable",
        "price": "19.99",
        "category": "peripherals",
        "description": "2m braided cable for high-refresh monitors.",
        "image": "/assets/DisplayPortCable.jpg",
        "rating": 4.6,
        "specs": ["2m Length", "Braided", "DisplayPort 2.1", "8K@60Hz"],
    },
    {
        "slug": "mouse-bungee",
        "name": "Mouse Bungee",
        "price": "9.49",
        "category": "peripherals",
        "description": "Spring-arm cable holder for smooth mouse movement.",
        "image": "/assets/MouseBungee.webp",
        "rating": 4.1,
        "specs": ["Spring-arm", "Non-slip Base", "Lightweight"],
        "stock": 2,
    },
    {
        "slug": "stream-deck",
        "name": "Stream Deck XL",
        "price": "199.99",
        "category": "peripherals",
        "description": "32 customizable LCD keys for streaming and productivity.",
        "image": "/assets/stream-deck.svg",
        "rating": 4.7,
        "specs": ["32 LCD Keys", "Customizable Profiles", "USB-C", "Plugin SDK Support"],
        "stock": 3,
    },
    {
        "slug": "gaming-chair",
        "name": "Apex Racing Chair",
        "price": "449.99",
        "category": "peripherals",
        "description": "Ergonomic racing-style chair with lumbar support and 4D armrests.",
        "image": "/assets/gaming-chair.svg",
        "rating": 4.5,
        "specs": ["PU Leather", "Lumbar Cushion", "4D Armrests", "180° Recline"],
    },
    {
        "slug": "cpu-cooler",
        "name": "Noctua NH-D15 Chromax",
        "price": "109.99",
        "category": "peripherals",
        "description": "Dual-tower air cooler with premium NF-A15 fans, silent operation.",
        "image": "/assets/cpu-cooler.svg",
        "rating": 4.9,
        "specs": ["Dual Tower", "NF-A15 Fans", "6 Heatpipes", "LGA1851 Compatible"],
        "stock": 0,
    },
    {
        "slug": "nvme-ssd",
        "name": "Samsung 990 Pro 2TB",
        "price": "189.99",
        "category": "peripherals",
        "description": "PCIe 4.0 NVMe M.2 SSD with blazing 7450MB/s read speeds.",
        "image": "/assets/nvme-ssd.svg",
        "rating": 4.8,
        "specs": ["2TB Capacity", "7450 MB/s Read", "PCIe 4.0", "Samsung V-NAND"],
    },
    {
        "slug": "sleeved-cables",
        "name": "CableMod Pro Sleeved Kit",
        "price": "79.99",
        "category": "peripherals",
        "description": "Premium paracord sleeved PSU cables with combs, full set.",
        "image": "/assets/sleeved-cables.svg",
        "rating": 4.3,
        "specs": ["Paracord Sleeving", "Cable Combs Included", "ATX 3.0 Compatible", "24-pin + 2x 8-pin"],
    },
    {
        "slug": "microphone",
        "name": "Elgato Wave:3",
        "price": "149.99",
        "category": "peripherals",
        "description": "Studio-quality USB condenser mic with Clipguard anti-distortion.",
        "image": "/assets/microphone.svg",
        "rating": 4.6,
        "specs": ["Condenser Capsule", "Clipguard Tech", "USB-C", "Wave Link Mixer"],
    },
]


ADDONS = [
    {"product_slug": "cyberpro-keyboard", "name": "Cleaning Kit", "description": "Microfiber cloth and keycap puller for easy maintenance.", "price": "9.99"},
    {"product_slug": "cyberpro-keyboard", "name": "Custom Keycap Set", "description": "PBT double-shot keycaps in retro beige.", "price": "29.99"},
    {"product_slug": "cyberpro-keyboard", "name": "Wrist Rest", "description": "Memory foam wrist rest with magnetic attachment.", "price": "14.99"},
    {"product_slug": "cyberpro-keyboard", "name": "USB-C Coiled Cable", "description": "Aviator-style coiled cable in matching color.", "price": "19.99"},
    {"product_slug": "gaming-mouse", "name": "Mouse Skates (PTFE)", "description": "Replacement pure PTFE mouse feet for smooth glide.", "price": "5.99"},
    {"product_slug": "gaming-mouse", "name": "Grip Tape Set", "description": "Pre-cut textured grip tape for side buttons and shell.", "price": "7.99"},
    {"product_slug": "gaming-mouse", "name": "Paracord Cable", "description": "Ultra-flexible paracord replacement cable.", "price": "8.99"},
    {"product_slug": "wireless-headset", "name": "Replacement Earpads", "description": "Memory foam velour earpads for comfort.", "price": "12.99"},
    {"product_slug": "wireless-headset", "name": "Charging Stand", "description": "Dedicated magnetic charging stand for headset.", "price": "24.99"},
    {"product_slug": "vanguard-desktop", "name": "Extended Warranty (2yr)", "description": "2-year extended warranty with on-site service.", "price": "99.99"},
    {"product_slug": "vanguard-desktop", "name": "RGB Light Strip Kit", "description": "Addressable RGB light strips with controller.", "price": "19.99"},
    {"product_slug": "ultrawide-monitor", "name": "Monitor Arm", "description": "Gas-spring monitor arm for ultrawide displays.", "price": "59.99"},
    {"product_slug": "ultrawide-monitor", "name": "Screen Cleaning Kit", "description": "Professional screen cleaner with microfiber cloth.", "price": "7.99"},
]


class Command(BaseCommand):
    help = "Seed the database with products from the frontend mock data"

    def handle(self, *args, **options):
        for data in PRODUCTS:
            category_slug = data.pop("category")
            category, _ = Category.objects.get_or_create(
                slug=category_slug,
                defaults={"name": category_slug.capitalize()},
            )
            Product.objects.update_or_create(
                slug=data["slug"],
                defaults={**data, "category": category},
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(PRODUCTS)} products"))

        addon_count = 0
        for addon_data in ADDONS:
            product_slug = addon_data.pop("product_slug")
            try:
                product = Product.objects.get(slug=product_slug)
            except Product.DoesNotExist:
                continue
            ProductAddon.objects.update_or_create(
                product=product,
                name=addon_data["name"],
                defaults={**addon_data},
            )
            addon_count += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {addon_count} product add-ons"))
