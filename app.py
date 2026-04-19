from fastapi import FastAPI, Header
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Self-hosted AI API is running"}

@app.post("/generate")
async def generate(data: dict, api_key: str = Header(None)):

    # API Key check
    if api_key != "mysecret123":
        return {"error": "Unauthorized"}

    prompt = data.get("prompt")

    if not prompt:
        return {"error": "Prompt is required"}

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",   # ✅ CHANGED HERE
                "prompt": prompt,
                "stream": False
            },
            timeout=420   # reasonable timeout
        )

        result = response.json()
        print("Ollama response:", result)

        # Handle response formats
        if "response" in result:
            output = result["response"]
        elif "message" in result:
            output = result["message"].get("content", "")
        else:
            output = ""

        output = output.replace("\n", " ").strip()

        if not output:
            return {"error": "Model did not return a response"}

        return {"response": output}

    except Exception as e:
        return {"error": str(e)}