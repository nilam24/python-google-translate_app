from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from deep_translator import GoogleTranslator

app = FastAPI()

class TranslateRequest(BaseModel):
    text: str
    target_lang: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Translate Clone</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; background: #f8f9fa; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 40px 20px; }
        h1 { color: #4285f4; margin-bottom: 30px; font-size: 2rem; }
        .container { background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 100%; max-width: 800px; padding: 30px; }
        .lang-bar { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
        select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; cursor: pointer; }
        .text-areas { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        textarea { width: 100%; height: 180px; padding: 14px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; resize: none; outline: none; }
        textarea:focus { border-color: #4285f4; }
        #output { background: #f8f9fa; color: #333; }
        button { margin-top: 20px; width: 100%; padding: 12px; background: #4285f4; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
        button:hover { background: #3367d6; }
        #error { color: red; margin-top: 10px; font-size: 14px; }
    </style>
</head>
<body>
    <h1>Translate</h1>
    <div class="container">
        <div class="lang-bar">
            <span>Detect language</span>
            <span>→</span>
            <select id="target_lang">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="zh-CN">Chinese</option>
                <option value="ar">Arabic</option>
                <option value="hi">Hindi</option>
                <option value="ja">Japanese</option>
                <option value="pt">Portuguese</option>
                <option value="ru">Russian</option>
            </select>
        </div>
        <div class="text-areas">
            <textarea id="input_text" placeholder="Enter text to translate..."></textarea>
            <textarea id="output" placeholder="Translation will appear here..." readonly></textarea>
        </div>
        <button onclick="doTranslate()">Translate</button>
        <p id="error"></p>
    </div>

    <script>
        async function doTranslate() {
            const text = document.getElementById("input_text").value.trim();
            const target_lang = document.getElementById("target_lang").value;
            const errorEl = document.getElementById("error");
            const outputEl = document.getElementById("output");

            errorEl.textContent = "";
            outputEl.value = "Translating...";

            if (!text) {
                errorEl.textContent = "Please enter some text.";
                outputEl.value = "";
                return;
            }

            try {
                const response = await fetch("/translate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text, target_lang })
                });
                const data = await response.json();
                if (data.result) {
                    outputEl.value = data.result;
                } else {
                    errorEl.textContent = data.error || "Translation failed.";
                    outputEl.value = "";
                }
            } catch (err) {
                errorEl.textContent = "Something went wrong. Try again.";
                outputEl.value = "";
            }
        }
    </script>
</body>
</html>
"""

@app.post("/translate")
def translate(req: TranslateRequest):
    try:
        translated = GoogleTranslator(source='auto', target=req.target_lang).translate(req.text)
        return {"result": translated}
    except Exception as e:
        return {"error": str(e)}
