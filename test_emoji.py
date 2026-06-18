from generate_pdf import strip_emojis

# Test emoji stripping
test_cases = [
    "HOTEL ENGLISH 🏨 All you need to know for travelling abroad 🇬🇧✈️",
    "Learn English in the Supermarket 🛒",
    "Hello World",
    "Test 🎉🎊 Party 🎈",
]

for title in test_cases:
    cleaned = strip_emojis(title)
    print(f"Original length: {len(title)}")
    print(f"Cleaned length: {len(cleaned)}")
    print(f"Cleaned text: {cleaned}")
    print("-" * 50)

# Test PDF generation
print("\nTesting PDF generation with emoji title...")
try:
    from generate_pdf import generate_pdf
    pairs = [("Hello", "你好"), ("World", "世界")]
    path = generate_pdf(pairs, "Test 🏨 Title ✈️", "Test Channel 🎉")
    print(f"[SUCCESS] PDF generated: {path}")
except Exception as e:
    print(f"[ERROR] {e}")