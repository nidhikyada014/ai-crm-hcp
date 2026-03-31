import requests

API_KEY ="your_gsk_key"

def call_llm(prompt):
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "gemma2-9b-it",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return res.json()["choices"][0]["message"]["content"]
