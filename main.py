from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="AI Multi-Agent Trading Advisor Coordinator")

def fetch_stock_data(symbol: str):
    """
    Simulates fetching live market statistics or pulling data from a financial API.
    You can later plug in Alpha Vantage or Yahoo Finance here.
    """
    # Mocking standard stock metrics for demonstration
    return {
        "symbol": symbol.upper(),
        "current_price": 2450.50,
        "rsi": 58.4,
        "volume_trend": "Above Average",
        "sector_sentiment": "Bullish"
    }

@app.get("/api/analyze")
def analyze_stock(symbol: str):
    if not symbol:
        raise HTTPException(status_code=400, detail="Stock symbol is required.")
    
    # Step 1: Gather raw market telemetry
    market = fetch_stock_data(symbol)
    
    # ----------------------------------------------------
    # AGENT 1: Technical Analysis Specialist
    # ----------------------------------------------------
    tech_commentary = (
        f"Technical Agent: Evaluated {market['symbol']}. "
        f"RSI is currently at {market['rsi']} (Neutral-to-Bullish zone). "
        f"Volume trend is registered as '{market['volume_trend']}', indicating steady buyer accumulation."
    )

    # ----------------------------------------------------
    # AGENT 2: Fundamental & Sentiment Specialist
    # ----------------------------------------------------
    sentiment_commentary = (
        f"Sentiment Agent: Market chatter and institutional liquidity flows "
        f"for {market['symbol']} are leaning {market['sector_sentiment']}. "
        f"Sector momentum remains supportive over a medium-term horizon."
    )

    # ----------------------------------------------------
    # AGENT 3: Risk Management & Final Synthesis Agent
    # ----------------------------------------------------
    risk_commentary = (
        f"Risk Management Agent: Based on inputs from Technical and Sentiment agents, "
        f"volatility is moderate. Suggested Action: Accumulate on pullbacks near support. "
        f"Maintain a strict stop-loss at 3% below entry to safeguard capital."
    )

    # Synthesizing the final multi-agent report
    final_report = (
        f"=== Multi-Agent AI Report: {market['symbol']} ===\n\n"
        f"💰 Current Reference Price: ₹{market['current_price']}\n\n"
        f"1️⃣ {tech_commentary}\n\n"
        f"2️⃣ {sentiment_commentary}\n\n"
        f"3️⃣ {risk_commentary}"
    )

    return {"recommendation": final_report}
  
