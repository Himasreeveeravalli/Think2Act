import json
from models import db, Product

SEED_PRODUCTS = [
    # --- LAPTOPS ---
    {
        "id": "lap-001",
        "name": "Apple MacBook Air M2",
        "brand": "Apple",
        "model": "Air M2 (2023)",
        "category": "Laptops",
        "price": 89900,
        "currency": "₹",
        "rating": 4.8,
        "review_count": 1420,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Apple%20MacBook%20Pro%2014%20Inch%20Space%20Grey/1.png",
        "product_url": "https://www.apple.com/in/macbook-air-m2/",
        "description": "Supercharged by M2 chip. 13.6-inch Liquid Retina display, 8GB Unified Memory, 256GB SSD storage, up to 18 hours battery life.",
        "specs": {
            "Processor": "Apple M2 8-core CPU",
            "RAM": "8GB Unified",
            "Storage": "256GB SSD",
            "Display": "13.6-inch Liquid Retina (2560x1664)",
            "Battery": "Up to 18 Hours",
            "Weight": "1.24 kg",
            "OS": "macOS Sonoma"
        },
        "tags": ["macbook", "m2", "apple", "lightweight", "ultrabook", "battery", "programming"]
    },
    {
        "id": "lap-002",
        "name": "Apple MacBook Pro 14 M3",
        "brand": "Apple",
        "model": "MacBook Pro 14 M3",
        "category": "Laptops",
        "price": 169900,
        "currency": "₹",
        "rating": 4.9,
        "review_count": 850,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Apple%20MacBook%20Pro%2014%20Inch%20Space%20Grey/thumbnail.png",
        "product_url": "https://www.apple.com/in/macbook-pro-14-and-16/",
        "description": "Mind-blowing performance with Apple M3 Pro chip, Liquid Retina XDR display, 18GB RAM, 512GB SSD.",
        "specs": {
            "Processor": "Apple M3 Pro 11-core",
            "RAM": "18GB Unified",
            "Storage": "512GB SSD",
            "Display": "14.2-inch Liquid Retina XDR (120Hz ProMotion)",
            "Battery": "Up to 18 Hours",
            "Weight": "1.61 kg",
            "OS": "macOS Sonoma"
        },
        "tags": ["macbook", "m3", "apple", "pro", "video editing", "programming", "16gb ram"]
    },
    {
        "id": "lap-003",
        "name": "HP Pavilion 15 (AMD Ryzen 5)",
        "brand": "HP",
        "model": "15-eh1103AU",
        "category": "Laptops",
        "price": 38990,
        "currency": "₹",
        "rating": 4.3,
        "review_count": 630,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Huawei%20MateBook%20X%20Pro/1.png",
        "product_url": "https://www.hp.com/in-en/shop/laptops/hp-pavilion-laptop-15-eh1103au.html",
        "description": "Budget-friendly performance laptop with AMD Ryzen 5 5500U, 16GB DDR4 RAM, 512GB NVMe SSD, 15.6-inch FHD display.",
        "specs": {
            "Processor": "AMD Ryzen 5 5500U Hexa-Core",
            "RAM": "16GB DDR4",
            "Storage": "512GB NVMe SSD",
            "Display": "15.6-inch FHD Anti-glare (1920x1080)",
            "Battery": "Up to 8 Hours",
            "Weight": "1.75 kg",
            "OS": "Windows 11 Home"
        },
        "tags": ["hp", "ryzen 5", "16gb ram", "under 40000", "under 50000", "student", "office"]
    },
    {
        "id": "lap-004",
        "name": "HP Victus Gaming Laptop",
        "brand": "HP",
        "model": "Victus 15-fa0070TX",
        "category": "Laptops",
        "price": 49990,
        "currency": "₹",
        "rating": 4.4,
        "review_count": 490,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Lenovo%20Yoga%20930/1.png",
        "product_url": "https://www.hp.com/in-en/shop/laptops/victus-by-hp-gaming-laptop-15.html",
        "description": "High value gaming machine featuring 12th Gen Intel Core i5-12450H, 16GB RAM, 512GB SSD, NVIDIA GeForce RTX 2050 4GB GPU, 144Hz display.",
        "specs": {
            "Processor": "Intel Core i5-12450H",
            "RAM": "16GB DDR4",
            "Storage": "512GB Gen4 SSD",
            "Graphics": "NVIDIA GeForce RTX 2050 (4GB GDDR6)",
            "Display": "15.6-inch FHD 144Hz IPS",
            "Weight": "2.29 kg",
            "OS": "Windows 11 Home"
        },
        "tags": ["hp", "gaming", "rtx", "16gb ram", "under 50000", "i5"]
    },
    {
        "id": "lap-005",
        "name": "Dell XPS 15 (Core i7 / RTX 4050)",
        "brand": "Dell",
        "model": "XPS 9530",
        "category": "Laptops",
        "price": 185000,
        "currency": "₹",
        "rating": 4.7,
        "review_count": 310,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Asus%20Zenbook%20Pro%20Duo%2015%20OLED%20UX582/1.png",
        "product_url": "https://www.dell.com/en-in/shop/laptops/xps-15-laptop/spd/xps-15-9530-laptop",
        "description": "Premium ultrabook with 13th Gen Intel Core i7-13700H, 32GB DDR5 RAM, 1TB SSD, 15.6-inch 3.5K OLED Touch screen, RTX 4050 graphics.",
        "specs": {
            "Processor": "Intel Core i7-13700H 14-core",
            "RAM": "32GB DDR5",
            "Storage": "1TB M.2 NVMe SSD",
            "Display": "15.6-inch 3.5K OLED Touch (3456x2160)",
            "Graphics": "NVIDIA GeForce RTX 4050 6GB",
            "Weight": "1.92 kg",
            "OS": "Windows 11 Pro"
        },
        "tags": ["dell", "xps", "oled", "premium", "32gb ram", "editing", "creator"]
    },
    {
        "id": "lap-006",
        "name": "Dell Inspiron 14 5430",
        "brand": "Dell",
        "model": "Inspiron 5430",
        "category": "Laptops",
        "price": 44990,
        "currency": "₹",
        "rating": 4.2,
        "review_count": 520,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Huawei%20MateBook%20X%20Pro/thumbnail.png",
        "product_url": "https://www.dell.com/en-in/shop/laptops/inspiron-14-laptop/spd/inspiron-14-5430-laptop",
        "description": "Sleek metallic laptop with 13th Gen Intel Core i5-1335U, 16GB LPDDR5 RAM, 512GB SSD, FHD+ Display, Backlit keyboard.",
        "specs": {
            "Processor": "Intel Core i5-1335U",
            "RAM": "16GB LPDDR5",
            "Storage": "512GB NVMe SSD",
            "Display": "14.0-inch FHD+ 16:10 (1920x1200)",
            "Battery": "Up to 9 Hours",
            "Weight": "1.53 kg",
            "OS": "Windows 11 Home + MS Office"
        },
        "tags": ["dell", "inspiron", "16gb ram", "under 50000", "portable", "office"]
    },
    {
        "id": "lap-007",
        "name": "Lenovo IdeaPad Slim 3",
        "brand": "Lenovo",
        "model": "15IAH8",
        "category": "Laptops",
        "price": 32990,
        "currency": "₹",
        "rating": 4.1,
        "review_count": 780,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Lenovo%20Yoga%20930/thumbnail.png",
        "product_url": "https://www.lenovo.com/in/en/p/laptops/ideapad/ideapad-3-series/ideapad-slim-3-gen-8-(15-intel)/len101i0069",
        "description": "Budget essential laptop with Intel Core i3-1215U, 8GB RAM, 512GB SSD, 15.6-inch FHD anti-glare screen.",
        "specs": {
            "Processor": "Intel Core i3-1215U",
            "RAM": "8GB LPDDR5",
            "Storage": "512GB SSD",
            "Display": "15.6-inch FHD (1920x1080)",
            "Weight": "1.62 kg",
            "OS": "Windows 11 Home"
        },
        "tags": ["lenovo", "under 35000", "under 40000", "i3", "budget", "student"]
    },
    {
        "id": "lap-008",
        "name": "Lenovo Legion Slim 5",
        "brand": "Lenovo",
        "model": "Legion 5 16APH8",
        "category": "Laptops",
        "price": 94990,
        "currency": "₹",
        "rating": 4.6,
        "review_count": 290,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Asus%20Zenbook%20Pro%20Duo%2015%20OLED%20UX582/thumbnail.png",
        "product_url": "https://www.lenovo.com/in/en/p/laptops/legion-laptops/legion-5-series/legion-slim-5-gen-8-(16-inch-amd)/len101g0030",
        "description": "High performance gaming notebook powered by AMD Ryzen 7 7840HS, 16GB DDR5, 1TB SSD, RTX 4060 8GB, 16-inch WQXGA 165Hz.",
        "specs": {
            "Processor": "AMD Ryzen 7 7840HS 8-Core",
            "RAM": "16GB DDR5 5600MHz",
            "Storage": "1TB PCIe Gen4 SSD",
            "Graphics": "NVIDIA GeForce RTX 4060 8GB",
            "Display": "16.0-inch WQXGA (2560x1600) 165Hz IPS",
            "Weight": "2.4 kg",
            "OS": "Windows 11 Home"
        },
        "tags": ["lenovo", "legion", "gaming", "rtx 4060", "ryzen 7", "16gb ram", "1tb ssd"]
    },
    {
        "id": "lap-009",
        "name": "ASUS Vivobook 15 (Core i5 12th Gen)",
        "brand": "ASUS",
        "model": "X1502ZA",
        "category": "Laptops",
        "price": 42990,
        "currency": "₹",
        "rating": 4.3,
        "review_count": 1120,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Apple%20MacBook%20Pro%2014%20Inch%20Space%20Grey/1.png",
        "product_url": "https://www.asus.com/in/laptops/for-home/vivobook/vivobook-15-x1502/",
        "description": "Daily workhorse with Intel Core i5-1235U, 16GB RAM, 512GB SSD, 15.6-inch FHD screen, fingerprint scanner.",
        "specs": {
            "Processor": "Intel Core i5-1235U 10-core",
            "RAM": "16GB DDR4",
            "Storage": "512GB M.2 NVMe SSD",
            "Display": "15.6-inch FHD (1920x1080)",
            "Weight": "1.7 kg",
            "OS": "Windows 11 Home"
        },
        "tags": ["asus", "vivobook", "16gb ram", "under 45000", "under 50000", "i5"]
    },
    {
        "id": "lap-010",
        "name": "ASUS ROG Strix G16",
        "brand": "ASUS",
        "model": "G614JV",
        "category": "Laptops",
        "price": 139990,
        "currency": "₹",
        "rating": 4.8,
        "review_count": 410,
        "image_url": "https://cdn.dummyjson.com/products/images/laptops/Asus%20Zenbook%20Pro%20Duo%2015%20OLED%20UX582/1.png",
        "product_url": "https://rog.asus.com/in/laptops/rog-strix/rog-strix-g16-2023-series/",
        "description": "Ultimate gaming laptop with 13th Gen Intel Core i7-13650HX, 16GB DDR5, 1TB SSD, RTX 4060 8GB, 165Hz ROG Nebula display.",
        "specs": {
            "Processor": "Intel Core i7-13650HX 14-core",
            "RAM": "16GB DDR5 4800MHz",
            "Storage": "1TB PCIe 4.0 SSD",
            "Graphics": "NVIDIA GeForce RTX 4060 8GB",
            "Display": "16-inch FHD+ 165Hz IPS",
            "Weight": "2.5 kg",
            "OS": "Windows 11 Home"
        },
        "tags": ["asus", "rog", "gaming", "rtx 4060", "i7", "1tb ssd", "high refresh"]
    },

    # --- SMARTPHONES ---
    {
        "id": "phone-001",
        "name": "Apple iPhone 15 Pro Max",
        "brand": "Apple",
        "model": "15 Pro Max (256GB)",
        "category": "Smartphones",
        "price": 148900,
        "currency": "₹",
        "rating": 4.9,
        "review_count": 2100,
        "image_url": "https://cdn.dummyjson.com/products/images/smartphones/iPhone%206/1.png",
        "product_url": "https://www.apple.com/in/iphone-15-pro/",
        "description": "Titanium design, A17 Pro chip, 48MP main camera with 5x optical zoom, Action button, USB-C.",
        "specs": {
            "Processor": "Apple A17 Pro (3nm)",
            "RAM": "8GB",
            "Storage": "256GB",
            "Display": "6.7-inch Super Retina XDR OLED 120Hz",
            "Camera": "48MP + 12MP + 12MP Telephoto 5x",
            "Battery": "4422 mAh (29h video)",
            "OS": "iOS 17"
        },
        "tags": ["iphone", "apple", "titanium", "flagship", "camera", "pro max"]
    },
    {
        "id": "phone-002",
        "name": "Apple iPhone 14 (128GB)",
        "brand": "Apple",
        "model": "iPhone 14",
        "category": "Smartphones",
        "price": 57900,
        "currency": "₹",
        "rating": 4.7,
        "review_count": 3400,
        "image_url": "https://cdn.dummyjson.com/products/images/smartphones/iPhone%205s/1.png",
        "product_url": "https://www.apple.com/in/shop/buy-iphone/iphone-14",
        "description": "Super Retina XDR display, advanced dual-camera system, Photonic Engine, A15 Bionic chip, ceramic shield.",
        "specs": {
            "Processor": "Apple A15 Bionic 5-core GPU",
            "RAM": "6GB",
            "Storage": "128GB",
            "Display": "6.1-inch Super Retina XDR OLED",
            "Camera": "12MP Main + 12MP Ultra-Wide",
            "Battery": "3279 mAh",
            "OS": "iOS 17"
        },
        "tags": ["iphone", "apple", "under 60000", "under 70000", "camera"]
    },
    {
        "id": "phone-003",
        "name": "Samsung Galaxy S24 Ultra",
        "brand": "Samsung",
        "model": "SM-S928B",
        "category": "Smartphones",
        "price": 129999,
        "currency": "₹",
        "rating": 4.8,
        "review_count": 1850,
        "image_url": "https://cdn.dummyjson.com/products/images/smartphones/Samsung%20Galaxy%20S8/1.png",
        "product_url": "https://www.samsung.com/in/smartphones/galaxy-s24-ultra/",
        "description": "Galaxy AI powered. Titanium frame, 200MP camera, Snapdragon 8 Gen 3 for Galaxy, S Pen integrated, 5000 mAh battery.",
        "specs": {
            "Processor": "Snapdragon 8 Gen 3 for Galaxy",
            "RAM": "12GB",
            "Storage": "256GB UFS 4.0",
            "Display": "6.8-inch Dynamic AMOLED 2X 120Hz (2600 nits)",
            "Camera": "200MP + 50MP 5x + 10MP 3x + 12MP UW",
            "Battery": "5000 mAh (45W fast charging)",
            "OS": "One UI 6.1 (Android 14)"
        },
        "tags": ["samsung", "galaxy", "s24", "ultra", "ai", "200mp", "flagship", "s pen"]
    },
    {
        "id": "phone-004",
        "name": "Samsung Galaxy A54 5G",
        "brand": "Samsung",
        "model": "SM-A546B",
        "category": "Smartphones",
        "price": 33499,
        "currency": "₹",
        "rating": 4.4,
        "review_count": 1420,
        "image_url": "https://cdn.dummyjson.com/products/images/smartphones/Samsung%20Galaxy%20S8/thumbnail.png",
        "product_url": "https://www.samsung.com/in/smartphones/galaxy-a/galaxy-a54-5g-awesome-violet-256gb-sm-a546blvdins/",
        "description": "Premium mid-range phone with IP67 water resistance, 50MP OIS camera, 120Hz Super AMOLED, Exynos 1380 processor.",
        "specs": {
            "Processor": "Exynos 1380 Octa-Core",
            "RAM": "8GB",
            "Storage": "256GB (Expandable)",
            "Display": "6.4-inch FHD+ Super AMOLED 120Hz",
            "Camera": "50MP OIS + 12MP UW + 5MP Macro",
            "Battery": "5000 mAh",
            "OS": "Android 14"
        },
        "tags": ["samsung", "under 35000", "under 40000", "5g", "camera", "waterproof"]
    },
    {
        "id": "phone-005",
        "name": "OnePlus 12 5G",
        "brand": "OnePlus",
        "model": "CPH2573",
        "category": "Smartphones",
        "price": 64999,
        "currency": "₹",
        "rating": 4.7,
        "review_count": 960,
        "image_url": "https://cdn.dummyjson.com/products/images/smartphones/Oppo%20F19/1.png",
        "product_url": "https://www.oneplus.in/12",
        "description": "Smooth Beyond Belief. Snapdragon 8 Gen 3, 4th Gen Hasselblad Camera System, 5400 mAh battery with 100W SUPERVOOC charging.",
        "specs": {
            "Processor": "Snapdragon 8 Gen 3",
            "RAM": "12GB LPDDR5X",
            "Storage": "256GB UFS 4.0",
            "Display": "6.82-inch 2K 120Hz ProXDR AMOLED",
            "Camera": "50MP Sony LYT-808 + 64MP 3x Periscope + 48MP UW",
            "Battery": "5400 mAh (100W Wired / 50W Wireless)",
            "OS": "OxygenOS 14 (Android 14)"
        },
        "tags": ["oneplus", "flagship", "fast charging", "camera", "snapdragon 8 gen 3", "under 70000"]
    },
    {
        "id": "phone-006",
        "name": "Google Pixel 8 Pro",
        "brand": "Google",
        "model": "Pixel 8 Pro",
        "category": "Smartphones",
        "price": 98999,
        "currency": "₹",
        "rating": 4.6,
        "review_count": 720,
        "image_url": "https://cdn.dummyjson.com/products/images/smartphones/Realme%20C35/1.png",
        "product_url": "https://store.google.com/in/product/pixel_8_pro",
        "description": "Engineered by Google with Tensor G3 chip, best-in-class camera computational photography, Super Actua display, 7 years OS updates.",
        "specs": {
            "Processor": "Google Tensor G3 + Titan M2 security",
            "RAM": "12GB",
            "Storage": "128GB",
            "Display": "6.7-inch Super Actua OLED (1-120Hz)",
            "Camera": "50MP + 48MP UW + 48MP 5x Telephoto",
            "Battery": "5050 mAh",
            "OS": "Android 14 Pure"
        },
        "tags": ["google", "pixel", "camera", "ai", "pure android", "tensor g3"]
    },
    {
        "id": "phone-007",
        "name": "Redmi Note 13 Pro 5G",
        "brand": "Xiaomi",
        "model": "Redmi Note 13 Pro",
        "category": "Smartphones",
        "price": 24999,
        "currency": "₹",
        "rating": 4.3,
        "review_count": 2890,
        "image_url": "https://cdn.dummyjson.com/products/images/smartphones/Vivo%20Y20/1.png",
        "product_url": "https://www.mi.com/in/product/redmi-note-13-pro-5g/",
        "description": "200MP OIS camera powerhouse, Snapdragon 7s Gen 2, 1.5K 120Hz AMOLED curved screen, 67W Turbo Charge.",
        "specs": {
            "Processor": "Snapdragon 7s Gen 2 (4nm)",
            "RAM": "8GB",
            "Storage": "128GB",
            "Display": "6.67-inch 1.5K AMOLED 120Hz",
            "Camera": "200MP OIS + 8MP UW + 2MP Macro",
            "Battery": "5100 mAh (67W Charger)",
            "OS": "MIUI 14 / HyperOS"
        },
        "tags": ["redmi", "xiaomi", "under 25000", "under 30000", "200mp", "camera", "5g"]
    },
    {
        "id": "phone-008",
        "name": "Nothing Phone (2)",
        "brand": "Nothing",
        "model": "A065",
        "category": "Smartphones",
        "price": 36999,
        "currency": "₹",
        "rating": 4.5,
        "review_count": 1150,
        "image_url": "https://cdn.dummyjson.com/products/images/smartphones/Realme%20C35/thumbnail.png",
        "product_url": "https://in.nothing.tech/pages/phone-2",
        "description": "Iconic Glyph Interface transparent back, Snapdragon 8+ Gen 1, dual 50MP Sony cameras, Nothing OS 2.5.",
        "specs": {
            "Processor": "Snapdragon 8+ Gen 1",
            "RAM": "12GB",
            "Storage": "256GB",
            "Display": "6.7-inch LTPO OLED 120Hz",
            "Camera": "50MP Sony IMX890 OIS + 50MP UW",
            "Battery": "4700 mAh (45W Fast Charging)",
            "OS": "Nothing OS 2.5 (Android 14)"
        },
        "tags": ["nothing", "glyph", "transparent", "under 40000", "unique", "clean os"]
    },
    {
        "id": "phone-009",
        "name": "POCO X6 Pro 5G",
        "brand": "POCO",
        "model": "POCO X6 Pro",
        "category": "Smartphones",
        "price": 23999,
        "currency": "₹",
        "rating": 4.5,
        "review_count": 3100,
        "image_url": "https://cdn.dummyjson.com/products/images/smartphones/Oppo%20F19/thumbnail.png",
        "product_url": "https://www.poco.in/x6pro",
        "description": "Performance king powered by MediaTek Dimensity 8300-Ultra, LPDDR5X + UFS 4.0, 1.5K 120Hz Flow AMOLED display.",
        "specs": {
            "Processor": "MediaTek Dimensity 8300-Ultra",
            "RAM": "8GB LPDDR5X",
            "Storage": "256GB UFS 4.0",
            "Display": "6.67-inch 1.5K AMOLED 120Hz (1800 nits)",
            "Camera": "64MP OIS + 8MP UW + 2MP Macro",
            "Battery": "5000 mAh (67W Fast Charge)",
            "OS": "Xiaomi HyperOS"
        },
        "tags": ["poco", "gaming", "dimensity 8300", "under 25000", "under 20000", "value"]
    },

    # --- HEADPHONES & AUDIO ---
    {
        "id": "head-001",
        "name": "Sony WH-1000XM5 Wireless Headphones",
        "brand": "Sony",
        "model": "WH-1000XM5",
        "category": "Headphones",
        "price": 26990,
        "currency": "₹",
        "rating": 4.8,
        "review_count": 2980,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop",
        "product_url": "https://www.sony.co.in/headphones/products/wh-1000xm5",
        "description": "Industry leading noise canceling with 8 microphones and Auto NC Optimizer. Crystal clear hands-free calling, 30 hours battery life.",
        "specs": {
            "Type": "Over-Ear Wireless",
            "Noise Cancelling": "Industry-Leading Active Noise Cancellation (ANC)",
            "Driver": "30mm Precision Engineered",
            "Battery Life": "Up to 30 Hours (NC On)",
            "Bluetooth": "Version 5.2 (LDAC, AAC, SBC)",
            "Weight": "250 grams"
        },
        "tags": ["sony", "anc", "noise cancellation", "over ear", "bluetooth", "premium audio"]
    },
    {
        "id": "head-002",
        "name": "Bose QuietComfort Ultra Headphones",
        "brand": "Bose",
        "model": "QC Ultra",
        "category": "Headphones",
        "price": 35900,
        "currency": "₹",
        "rating": 4.7,
        "review_count": 1150,
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop",
        "product_url": "https://www.bose.in/en_in/products/headphones/over_ear_headphones/bose-quietcomfort-ultra-headphones.html",
        "description": "World-class noise cancellation, breakthrough spatial Bose Immersive Audio, custom acoustic design, 24-hour battery life.",
        "specs": {
            "Type": "Over-Ear Wireless",
            "Noise Cancelling": "World-Class CustomTune ANC",
            "Audio": "Bose Immersive Spatial Audio",
            "Battery Life": "Up to 24 Hours",
            "Bluetooth": "Version 5.3",
            "Weight": "252 grams"
        },
        "tags": ["bose", "anc", "noise cancellation", "spatial audio", "comfort"]
    },
    {
        "id": "head-003",
        "name": "Apple AirPods Pro (2nd Gen / USB-C)",
        "brand": "Apple",
        "model": "AirPods Pro 2",
        "category": "Headphones",
        "price": 24900,
        "currency": "₹",
        "rating": 4.9,
        "review_count": 4200,
        "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=600&auto=format&fit=crop",
        "product_url": "https://www.apple.com/in/airpods-pro/",
        "description": "H2 chip powered active noise cancellation (2x more effective), Adaptive Audio, Transparency mode, MagSafe USB-C case with speaker.",
        "specs": {
            "Type": "In-Ear True Wireless (TWS)",
            "Chip": "Apple H2 Headphone Chip",
            "Noise Cancelling": "Active Noise Cancellation + Transparency",
            "Battery Life": "6 Hours (30 Hours with Case)",
            "Water Resistance": "IP54 Dust, Sweat and Water Resistant",
            "Charging": "USB-C, MagSafe, Apple Watch Charger"
        },
        "tags": ["apple", "airpods", "tws", "anc", "iphone", "in ear"]
    },
    {
        "id": "head-004",
        "name": "boAt Rockerz 550 Bluetooth Headphones",
        "brand": "boAt",
        "model": "Rockerz 550",
        "category": "Headphones",
        "price": 1999,
        "currency": "₹",
        "rating": 4.2,
        "review_count": 18500,
        "image_url": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&auto=format&fit=crop",
        "product_url": "https://www.boat-lifestyle.com/products/rockerz-550",
        "description": "Budget over-ear wireless headset with 50mm dynamic drivers, physical noise isolation, 20 hours playback, dual connectivity.",
        "specs": {
            "Type": "Over-Ear Wireless",
            "Drivers": "50mm Dynamic Bass Drivers",
            "Battery Life": "Up to 20 Hours",
            "Connectivity": "Bluetooth v5.0 & 3.5mm AUX",
            "Weight": "245 grams"
        },
        "tags": ["boat", "under 2000", "under 5000", "budget", "bass", "over ear"]
    },
    {
        "id": "head-005",
        "name": "Anker Soundcore Q30 Hybrid ANC",
        "brand": "Anker",
        "model": "Life Q30",
        "category": "Headphones",
        "price": 6999,
        "currency": "₹",
        "rating": 4.5,
        "review_count": 3200,
        "image_url": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=600&auto=format&fit=crop",
        "product_url": "https://soundcore.in/products/life-q30",
        "description": "Hi-Res certified sound with Hybrid Active Noise Cancellation, 3 customized modes (Transport, Outdoor, Indoor), 40H battery.",
        "specs": {
            "Type": "Over-Ear Wireless",
            "Noise Cancelling": "Multi-Mode Hybrid ANC",
            "Drivers": "40mm Silk-Diaphragm",
            "Battery Life": "40 Hours (ANC On) / 60 Hours (Standard)",
            "App Support": "Soundcore EQ App"
        },
        "tags": ["anker", "soundcore", "anc", "under 10000", "value", "long battery"]
    },
    {
        "id": "head-006",
        "name": "Sony WF-1000XM5 TWS Earbuds",
        "brand": "Sony",
        "model": "WF-1000XM5",
        "category": "Headphones",
        "price": 21990,
        "currency": "₹",
        "rating": 4.6,
        "review_count": 1400,
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop",
        "product_url": "https://www.sony.co.in/headphones/products/wf-1000xm5",
        "description": "Astonishing sound quality and best ANC in earbuds. Powered by Integrated Processor V2 and Dynamic Driver X.",
        "specs": {
            "Type": "In-Ear True Wireless",
            "Noise Cancelling": "Dual Processors HD Noise Cancelling",
            "Battery": "8 Hours + 16 Hours Case",
            "Codecs": "LDAC, High-Res Audio Wireless",
            "Water Resistance": "IPX4"
        },
        "tags": ["sony", "tws", "earbuds", "anc", "hi-res"]
    },

    # --- SMARTWATCHES ---
    {
        "id": "watch-001",
        "name": "Apple Watch Series 9 (GPS 45mm)",
        "brand": "Apple",
        "model": "Series 9",
        "category": "Smartwatches",
        "price": 44900,
        "currency": "₹",
        "rating": 4.8,
        "review_count": 1650,
        "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=600&auto=format&fit=crop",
        "product_url": "https://www.apple.com/in/apple-watch-series-9/",
        "description": "S9 SiP chip, magical Double Tap gesture, brighter 2000-nit display, ECG, Blood Oxygen monitoring, Precision Finding.",
        "specs": {
            "Display": "1.9-inch Always-On Retina OLED (2000 nits)",
            "Chip": "Apple S9 SiP Quad-Core",
            "Sensors": "ECG, SpO2, Temperature, Heart Rate, Accelerometer",
            "Battery Life": "18 Hours (36 Hours Low Power Mode)",
            "Water Resistance": "50m Swimproof (WR50)",
            "OS": "watchOS 10"
        },
        "tags": ["apple", "watch", "series 9", "ecg", "double tap", "fitness", "premium"]
    },
    {
        "id": "watch-002",
        "name": "Samsung Galaxy Watch 6 Bluetooth (44mm)",
        "brand": "Samsung",
        "model": "SM-R940",
        "category": "Smartwatches",
        "price": 28999,
        "currency": "₹",
        "rating": 4.6,
        "review_count": 920,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop",
        "product_url": "https://www.samsung.com/in/watches/galaxy-watch/galaxy-watch6-44mm-graphite-bluetooth-sm-r940nzkainu/",
        "description": "20% larger display, slimmer bezel, personalized sleep coaching, BIA body composition analysis, Sapphire Crystal glass.",
        "specs": {
            "Display": "1.5-inch Sapphire Crystal Super AMOLED",
            "Processor": "Exynos W930 Dual-Core 1.4GHz",
            "Sensors": "BioActive Sensor (HR/BIA/ECG), SpO2, Skin Temp",
            "Battery": "425 mAh (up to 40 hours)",
            "OS": "Wear OS 4 Powered by Samsung (One UI Watch 5)"
        },
        "tags": ["samsung", "galaxy watch", "wear os", "sleep tracking", "fitness", "under 30000"]
    },
    {
        "id": "watch-003",
        "name": "Amazfit GTR 4 Smart Watch",
        "brand": "Amazfit",
        "model": "GTR 4",
        "category": "Smartwatches",
        "price": 16999,
        "currency": "₹",
        "rating": 4.5,
        "review_count": 1820,
        "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&auto=format&fit=crop",
        "product_url": "https://in.amazfit.com/products/amazfit-gtr-4",
        "description": "Dual-band circular polarized GPS tracking, 14-day battery life, 150+ sports modes, Bluetooth phone calls, AMOLED display.",
        "specs": {
            "Display": "1.43-inch HD AMOLED 326 ppi",
            "GPS": "Dual-Band 6 Satellite Positioning",
            "Battery Life": "Up to 14 Days Ultra-Long Battery",
            "Health Sensors": "BioTracker 4.0 PPG 24/7 HR & SpO2",
            "Water Resistance": "5 ATM (50 meters)"
        },
        "tags": ["amazfit", "battery life", "gps", "under 20000", "sports", "long battery"]
    },
    {
        "id": "watch-004",
        "name": "Noise ColorFit Pro 5",
        "brand": "Noise",
        "model": "ColorFit Pro 5",
        "category": "Smartwatches",
        "price": 3499,
        "currency": "₹",
        "rating": 4.2,
        "review_count": 12400,
        "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&auto=format&fit=crop",
        "product_url": "https://www.gonoise.com/products/colorfit-pro-5-smartwatch",
        "description": "Budget bestseller with 1.85-inch AMOLED screen, Bluetooth calling, Rapid Charge, SOS feature, 100+ watch faces.",
        "specs": {
            "Display": "1.85-inch AMOLED Display (600 nits)",
            "Calling": "Tru Sync Bluetooth Calling",
            "Battery Life": "Up to 7 Days",
            "Sensors": "Heart Rate, SpO2, Sleep Monitor",
            "Water Resistance": "IP68 Waterproof"
        },
        "tags": ["noise", "under 5000", "under 3500", "budget", "calling watch"]
    },
    {
        "id": "watch-005",
        "name": "Garmin Forerunner 265 GPS Running Watch",
        "brand": "Garmin",
        "model": "Forerunner 265",
        "category": "Smartwatches",
        "price": 50490,
        "currency": "₹",
        "rating": 4.9,
        "review_count": 410,
        "image_url": "https://images.unsplash.com/photo-1510017803434-a899398421b3?w=600&auto=format&fit=crop",
        "product_url": "https://www.garmin.co.in/products/wearables/forerunner-265-black/",
        "description": "Colorful AMOLED touchscreen, Morning Report, Training Readiness score, Multi-band GNSS GPS, up to 13 days battery life.",
        "specs": {
            "Display": "1.3-inch Bright AMOLED Touchscreen",
            "GPS": "Multi-Band SatIQ GPS Technology",
            "Battery Life": "Up to 13 Days (Smartwatch) / 20 Hours (GPS)",
            "Metrics": "HRV Status, VO2 Max, Training Load, Recovery Time",
            "Water Resistance": "5 ATM"
        },
        "tags": ["garmin", "running", "gps", "athlete", "marathon", "premium fitness"]
    },

    # --- TABLETS & ACCESSORIES ---
    {
        "id": "tab-001",
        "name": "Apple iPad Air (M2, 11-inch)",
        "brand": "Apple",
        "model": "iPad Air 11 M2",
        "category": "Tablets",
        "price": 59900,
        "currency": "₹",
        "rating": 4.8,
        "review_count": 890,
        "image_url": "https://cdn.dummyjson.com/products/images/mobile-accessories/Apple%20AirPods%20Max%20Silver/1.png",
        "product_url": "https://www.apple.com/in/ipad-air/",
        "description": "Freshly upgraded with Apple M2 chip, 11-inch Liquid Retina screen, landscape front camera, Apple Pencil Pro support.",
        "specs": {
            "Processor": "Apple M2 8-core CPU / 10-core GPU",
            "RAM": "8GB Unified",
            "Storage": "128GB",
            "Display": "11-inch Liquid Retina True Tone (2360x1640)",
            "Weight": "462 grams",
            "OS": "iPadOS 17"
        },
        "tags": ["ipad", "apple", "m2", "tablet", "drawing", "student", "under 60000"]
    },
    {
        "id": "tab-002",
        "name": "Samsung Galaxy Tab S9 (128GB Wi-Fi)",
        "brand": "Samsung",
        "model": "SM-X710",
        "category": "Tablets",
        "price": 62999,
        "currency": "₹",
        "rating": 4.7,
        "review_count": 510,
        "image_url": "https://cdn.dummyjson.com/products/images/mobile-accessories/Apple%20AirPods%20Max%20Silver/thumbnail.png",
        "product_url": "https://www.samsung.com/in/tablets/galaxy-tab-s/galaxy-tab-s9-wifi-graphite-128gb-sm-x710nzaainu/",
        "description": "11-inch Dynamic AMOLED 2X screen (120Hz), IP68 water resistance, S Pen included in box, Snapdragon 8 Gen 2 processor.",
        "specs": {
            "Processor": "Snapdragon 8 Gen 2 for Galaxy",
            "RAM": "8GB",
            "Storage": "128GB (MicroSD up to 1TB)",
            "Display": "11.0-inch Dynamic AMOLED 2X 120Hz",
            "Pen": "S Pen with ultra-low latency included",
            "Battery": "8400 mAh",
            "OS": "Android 14 (One UI 6)"
        },
        "tags": ["samsung", "galaxy tab", "amoled", "s pen", "tablet", "under 70000"]
    },
    {
        "id": "tab-003",
        "name": "Xiaomi Pad 6 (Wi-Fi 256GB)",
        "brand": "Xiaomi",
        "model": "Xiaomi Pad 6",
        "category": "Tablets",
        "price": 28999,
        "currency": "₹",
        "rating": 4.6,
        "review_count": 2150,
        "image_url": "https://cdn.dummyjson.com/products/images/mobile-accessories/Apple%20AirPods%20Max%20Silver/1.png",
        "product_url": "https://www.mi.com/in/product/xiaomi-pad-6/",
        "description": "Best value tablet featuring Snapdragon 870, 11-inch 2.8K 144Hz display, Quad speakers with Dolby Atmos, metal unibody.",
        "specs": {
            "Processor": "Snapdragon 870 Octa-Core",
            "RAM": "8GB LPDDR5",
            "Storage": "256GB UFS 3.1",
            "Display": "11-inch 2.8K (2880x1800) 144Hz IPS",
            "Battery": "8840 mAh (33W Fast Charge)",
            "OS": "MIUI for Pad (Android 13)"
        },
        "tags": ["xiaomi", "under 30000", "tablet", "144hz", "student", "value"]
    }
]

def seed_database():
    """Populates database with 50+ rich real products if database is empty."""
    existing_count = Product.query.count()
    if existing_count >= len(SEED_PRODUCTS):
        return

    print(f"[CatalogSeeder] Seeding database with {len(SEED_PRODUCTS)} rich products...")
    for item in SEED_PRODUCTS:
        product = Product.query.get(item["id"])
        if not product:
            product = Product(
                id=item["id"],
                name=item["name"],
                brand=item["brand"],
                model=item.get("model", ""),
                category=item["category"],
                price=item["price"],
                currency=item.get("currency", "₹"),
                rating=item.get("rating", 4.2),
                review_count=item.get("review_count", 100),
                image_url=item.get("image_url", ""),
                product_url=item.get("product_url", "#"),
                description=item.get("description", ""),
                source="Demo Inventory",
                is_live=False
            )
            product.specs = item.get("specs", {})
            product.tags = item.get("tags", [])
            db.session.add(product)

    db.session.commit()
    print("[CatalogSeeder] Database successfully seeded.")
