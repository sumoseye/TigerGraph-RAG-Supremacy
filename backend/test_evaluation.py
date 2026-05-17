import requests
import json

url = "http://localhost:8000/api/evaluate"

payload = {
    "query": "What are the latest advances in quantum computing?",
    "ground_truth": json.dumps({
        "correct_answer": "Recent quantum computing advances include improvements in error correction, increased qubit counts, and better coherence times."
    })
}

print("Sending evaluation request...")
response = requests.post(url, json=payload, timeout=120)

print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))