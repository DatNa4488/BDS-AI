import requests
import json

url = "http://localhost:8000/api/v1/search"
payload = {
    "query": "Nhà 3 tầng Cầu Giấy dưới 5 tỷ",
    "search_realtime": True,
    "max_results": 5
}

print("Sending request to:", url)
print("Payload:", json.dumps(payload, indent=2, ensure_ascii=False))

try:
    response = requests.post(url, json=payload, timeout=120)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'response'):
        print(f"Response text: {e.response.text}")
