from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email Triage Environment</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background: #1e293b;
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                max-width: 600px;
                text-align: center;
            }
            h1 {
                margin-bottom: 1rem;
            }
            p {
                color: #cbd5e1;
            }
            code {
                background: #334155;
                padding: 4px 8px;
                border-radius: 6px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Email Triage Environment</h1>
            <p>Your OpenEnv environment is running successfully.</p>
            <p>API status: <code>OK</code></p>
            <p>Version: <code>1.0.0</code></p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "ok", "name": "Email Triage Environment", "version": "1.0.0"}

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()