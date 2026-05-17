# backend/test_hf_directly.py
import os
from app.config import settings

print(f"HF_TOKEN: {settings.HF_TOKEN}")
print(f"Token length: {len(settings.HF_TOKEN) if settings.HF_TOKEN else 0}")

if settings.HF_TOKEN:
    try:
        from huggingface_hub import InferenceClient
        
        print("\nTesting Hugging Face connection...")
        client = InferenceClient(
            model="meta-llama/Llama-3.1-8B-Instruct",
            token=settings.HF_TOKEN
        )
        print("✅ Client created successfully!")
        
        # Try a simple request
        print("\nTesting API call...")
        response = client.chat_completion(
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=10
        )
        print(f"✅ API works!")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ HF_TOKEN not set")