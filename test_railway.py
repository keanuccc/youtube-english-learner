import requests
import sys

# Test Railway connection
print("Testing Railway connection...")

# You need to replace this with your actual Railway URL
railway_url = input("Enter your Railway URL (or press Enter for localhost:5000): ").strip()
if not railway_url:
    railway_url = "http://localhost:5000"

try:
    # Test health endpoint
    print(f"\nTesting: {railway_url}/api/health")
    r = requests.get(f"{railway_url}/api/health", timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")

    if r.status_code == 200:
        print("\n✓ Backend is running!")

        # Test with a sample YouTube URL
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        print(f"\nTesting generate endpoint with: {test_url}")

        r2 = requests.post(
            f"{railway_url}/api/generate",
            json={"url": test_url},
            timeout=30
        )
        print(f"Status: {r2.status_code}")
        print(f"Response: {r2.text[:200]}...")
    else:
        print("\n✗ Backend returned error status")

except requests.exceptions.ConnectionError:
    print(f"\n✗ Cannot connect to {railway_url}")
    print("  - Check if the server is running")
    print("  - Check if the URL is correct")
except requests.exceptions.Timeout:
    print(f"\n✗ Connection timed out")
except Exception as e:
    print(f"\n✗ Error: {e}")