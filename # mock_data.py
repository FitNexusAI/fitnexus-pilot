# mock_data.py

# This simulates the "Secure Processing" of store data
PRODUCT_NAME = "Luxe High-Waist Wide Leg Trousers"

# Simulating unstructured raw reviews from a Shopify/Magento store
RAW_REVIEWS = [
    {
        "id": "R001",
        "customer_id": "anon_123", # Anonymized
        "rating": 4,
        "text": "Love the fabric, it feels very premium. However, the waist is incredibly tight. I usually wear a Medium but could barely button it.",
        "size_purchased": "M"
    },
    {
        "id": "R002",
        "customer_id": "anon_456",
        "rating": 5,
        "text": "Perfect length for tall girls! I'm 5'10 and these hit the floor perfectly. The color is exactly like the picture.",
        "size_purchased": "L"
    },
    {
        "id": "R003",
        "customer_id": "anon_789",
        "rating": 3,
        "text": "Good quality but runs very small. Definitely size up if you have hips. The zipper feels a bit fragile too.",
        "size_purchased": "S"
    },
    {
        "id": "R004",
        "customer_id": "anon_101",
        "rating": 2,
        "text": "Way too long. I'm 5'4 and I'd need to hem 3 inches off. Returns are a hassle.",
        "size_purchased": "M"
    }
]

# The Brand Voice Guidelines (for the generated Fit Note)
BRAND_VOICE = """
Tone: Helpful, transparent, and concise. 
Goal: Reduce returns by setting clear expectations.
Keywords to use: 'True to size', 'Size up', 'Fabric stretch'.
"""