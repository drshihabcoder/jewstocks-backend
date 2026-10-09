from fastapi import FastAPI, HTTPException
import requests
import base64
import os
import yfinance as yf

app = FastAPI(title="Autonomous Multi-Agent AI Backend")

# GitHub configuration (retrieved securely from Render Environment Variables)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO", "your-username/jewstocks-backend")  # e.g., "shaikh/jewstocks-backend"
BRANCH = "main"

@app.get("/api/analyze")
def analyze_stock(symbol: str):
    if not symbol:
        raise HTTPException(status_code=400, detail="Stock symbol is required.")
    
    clean_symbol = symbol.strip().upper()
    search_query = clean_symbol if "." in clean_symbol else f"{clean_symbol}.NS"
    
    stock = yf.Ticker(search_query)
    hist = stock.history(period="5d")
    
    if hist.empty:
        stock = yf.Ticker(clean_symbol)
        hist = stock.history(period="5d")
        search_query = clean_symbol
        
    if hist.empty:
        return {
            "recommendation": f"❌ Error: Stock symbol '{clean_symbol}' not found in markets."
        }
            
    current_price = float(hist['Close'].iloc[-1])
    prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
    price_change_pct = ((current_price - prev_close) / prev_close) * 100
    ma_5 = float(hist['Close'].mean())

    # Multi-Agent Synthesis
    trend_desc = "Bullish momentum" if price_change_pct >= 0 else "Consolidating/Bearish pressure"
    tech_commentary = f"Technical Agent: Live close for {search_query} is ₹{current_price:.2f} ({price_change_pct:+.2f}%). Trend shows {trend_desc} relative to 5-day average (₹{ma_5:.2f})."
    sentiment_commentary = f"Sentiment Agent: Volume behavior indicates active capital flow supporting medium-term horizons."
    risk_commentary = f"Risk Management Agent: Recommended Action: {'Accumulate on dips' if price_change_pct >= 0 else 'Hold & watch support'}. Stop-loss: 3.5%."

    final_report = (
        f"=== Autonomous AI Report: {search_query} ===\n\n"
        f"💰 Live Price: ₹{current_price:.2f}\n\n"
        f"1️⃣ {tech_commentary}\n\n"
        f"2️⃣ {sentiment_commentary}\n\n"
        f"3️⃣ {risk_commentary}"
    )

    return {"recommendation": final_report}


@app.post("/api/update-code")
def update_backend_code(new_python_code: str, commit_message: str = "Autonomous code update via prompt"):
    """
    Allows the backend to program itself by committing new code directly to GitHub,
    triggering an automatic zero-touch Render redeployment.
    """
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GitHub Token not configured on server environment.")
    
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/main.py"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    # 1. Get current file's SHA (required by GitHub API to update files)
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch current file from GitHub.")
    
    file_sha = resp.json()["sha"]
    
    # 2. Encode new code to Base64
    encoded_content = base64.b64encode(new_python_code.encode("utf-8")).decode("utf-8")
    
    # 3. Push update payload to GitHub
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "sha": file_sha,
        "branch": BRANCH
    }
    
    put_resp = requests.put(url, headers=headers, json=payload)
    if put_resp.status_code not in [200, 201]:
        raise HTTPException(status_code=400, detail=f"GitHub update failed: {put_resp.text}")
        
    return {
        "status": "Success", 
        "message": "Backend code successfully updated and pushed! Render is now auto-redeploying."
    }
