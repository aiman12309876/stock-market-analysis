import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

def get_stock_data(symbol, period="6mo"):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data

def calculate_support_resistance(data, window=20):
    high = data['High'].rolling(window=window).max()
    low = data['Low'].rolling(window=window).min()
    return low, high

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_moving_averages(data):
    ma50 = data['Close'].rolling(window=50).mean()
    ma200 = data['Close'].rolling(window=200).mean()
    return ma50, ma200

def analyze_trend(data):
    last_close = data['Close'].iloc[-1]
    ma50, ma200 = calculate_moving_averages(data)
    
    if last_close > ma50.iloc[-1] and ma50.iloc[-1] > ma200.iloc[-1]:
        trend = "BULLISH"
    elif last_close < ma50.iloc[-1] and ma50.iloc[-1] < ma200.iloc[-1]:
        trend = "BEARISH"
    else:
        trend = "NEUTRAL"
    
    return trend, ma50, ma200

def find_levels(data, window=20):
    support, resistance = calculate_support_resistance(data, window)
    current_price = data['Close'].iloc[-1]
    
    nearest_support = support[support < current_price].max()
    nearest_resistance = resistance[resistance > current_price].min()
    
    return nearest_support, nearest_resistance

def plot_analysis(data, ma50, ma200, rsi, support, resistance):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Price Chart
    ax1.plot(data.index, data['Close'], label='Close Price', color='black', linewidth=1.5)
    ax1.plot(data.index, ma50, label='50-day MA', color='blue', linestyle='--', linewidth=1.5)
    ax1.plot(data.index, ma200, label='200-day MA', color='red', linestyle='--', linewidth=1.5)
    
    # Support and Resistance
    ax1.axhline(y=support, color='green', linestyle='-', linewidth=1, label='Support')
    ax1.axhline(y=resistance, color='red', linestyle='-', linewidth=1, label='Resistance')
    
    ax1.set_title('Technical Analysis - Price Action with Support/Resistance')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # RSI Chart
    ax2.plot(data.index, rsi, label='RSI', color='purple', linewidth=1.5)
    ax2.axhline(y=70, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax2.axhline(y=30, color='green', linestyle='--', linewidth=1, alpha=0.7)
    ax2.fill_between(data.index, 30, 70, alpha=0.1, color='gray')
    ax2.set_title('Relative Strength Index (RSI)')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def generate_report(data, trend, support, resistance, rsi):
    print("\n" + "=" * 60)
    print("        TECHNICAL ANALYSIS REPORT")
    print("=" * 60)
    
    current_price = data['Close'].iloc[-1]
    print(f"Current Price: ${current_price:.2f}")
    print(f"Trend: {trend}")
    print(f"Nearest Support: ${support:.2f}" if not pd.isna(support) else "Nearest Support: N/A")
    print(f"Nearest Resistance: ${resistance:.2f}" if not pd.isna(resistance) else "Nearest Resistance: N/A")
    
    last_rsi = rsi.iloc[-1]
    if last_rsi > 70:
        rsi_status = "OVERSOLD"
    elif last_rsi < 30:
        rsi_status = "OVERBOUGHT"
    else:
        rsi_status = "NEUTRAL"
    print(f"RSI: {last_rsi:.2f} ({rsi_status})")
    
    print("\n" + "=" * 60)
    print("           RECOMMENDATION")
    print("=" * 60)
    
    if trend == "BULLISH" and last_rsi < 70:
        print("Consider BUYING on pullbacks to support levels.")
    elif trend == "BEARISH" and last_rsi > 30:
        print("Consider SELLING on rallies to resistance levels.")
    else:
        print("WAIT for clearer signals.")
    print("=" * 60)

def main():
    print("\n" + "=" * 60)
    print("     STOCK MARKET TECHNICAL ANALYSIS")
    print("=" * 60)
    
    symbol = input("Enter stock symbol (e.g., AAPL, TSLA): ").upper()
    
    try:
        data = get_stock_data(symbol)
        
        if data.empty:
            print("No data found. Please check the symbol.")
            return
        
        print(f"\nAnalyzing {symbol}...")
        
        rsi = calculate_rsi(data)
        ma50, ma200 = calculate_moving_averages(data)
        trend, ma50, ma200 = analyze_trend(data)
        support, resistance = find_levels(data)
        
        generate_report(data, trend, support, resistance, rsi)
        plot_analysis(data, ma50, ma200, rsi, support, resistance)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()