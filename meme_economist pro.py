import streamlit as st
import pandas as pd
import random
import requests
import time
from datetime import datetime

# Page config
st.set_page_config(page_title="Meme Economist Pro", layout="wide")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.memes = {
        'Wojak': {'price': 100.00, 'volatility': 0.2, 'mentions': 0},
        'Dogecoin': {'price': 50.00, 'volatility': 0.3, 'mentions': 0},
        'Distracted Boyfriend': {'price': 75.00, 'volatility': 0.15, 'mentions': 0},
        'Pepe the Frog': {'price': 120.00, 'volatility': 0.25, 'mentions': 0},
        'Drake Template': {'price': 80.00, 'volatility': 0.22, 'mentions': 0}
    }
    st.session_state.cash = 10000.00
    st.session_state.portfolio = {meme: 0 for meme in st.session_state.memes}
    st.session_state.trade_history = []
    st.session_state.round = 1
    st.session_state.initialized = True

def fetch_reddit_mentions(meme_name):
    """Simulate fetching real Reddit data (we'll use mock data for now)"""
    # Mock API response - in production, use: https://www.reddit.com/dev/api/
    time.sleep(0.1)  # Simulate API delay
    return random.randint(0, 50)  # Mock mention count

def update_prices_with_real_data():
    """Update prices based on simulated real-world data"""
    for meme, data in st.session_state.memes.items():
        # Get simulated "real" mentions
        mentions = fetch_reddit_mentions(meme)
        st.session_state.memes[meme]['mentions'] = mentions
        
        # Price change based on mentions + volatility
        mention_effect = min(mentions * 0.001, 0.1)  # Max 10% effect from mentions
        volatility_effect = random.uniform(-data['volatility'], data['volatility'])
        
        total_change = mention_effect + volatility_effect
        
        # Big market events (2% chance)
        if random.random() < 0.02:
            total_change *= 4  # 4x movement for viral events!
        
        new_price = max(0.01, data['price'] * (1 + total_change))
        st.session_state.memes[meme]['price'] = round(new_price, 2)
        st.session_state.memes[meme]['change'] = total_change * 100

def buy_meme(meme, quantity):
    price = st.session_state.memes[meme]['price']
    cost = price * quantity
    if st.session_state.cash >= cost:
        st.session_state.cash -= cost
        st.session_state.portfolio[meme] += quantity
        st.session_state.trade_history.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'action': 'BUY',
            'meme': meme,
            'quantity': quantity,
            'price': price,
            'total': cost
        })
        return True
    return False

def sell_meme(meme, quantity):
    if st.session_state.portfolio[meme] >= quantity:
        price = st.session_state.memes[meme]['price']
        revenue = price * quantity
        st.session_state.cash += revenue
        st.session_state.portfolio[meme] -= quantity
        st.session_state.trade_history.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'action': 'SELL',
            'meme': meme,
            'quantity': quantity,
            'price': price,
            'total': revenue
        })
        return True
    return False

# UI Layout
st.title("🚀 Meme Economist Pro")
st.markdown("**Real-time meme trading powered by social data**")

# Main columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Live Market")
    
    # Market data table
    market_data = []
    for meme, data in st.session_state.memes.items():
        change = data.get('change', 0)
        change_icon = "🟢" if change > 0 else "🔴"
        market_data.append({
            'Meme': meme,
            'Price': f"${data['price']:.2f}",
            'Change': f"{change_icon} {change:+.1f}%",
            'Mentions': data['mentions'],
            'Volatility': f"{data['volatility']*100:.0f}%"
        })
    
    st.dataframe(pd.DataFrame(market_data), use_container_width=True)

with col2:
    st.subheader("💰 Your Portfolio")
    
    portfolio_value = st.session_state.cash
    for meme, shares in st.session_state.portfolio.items():
        if shares > 0:
            value = shares * st.session_state.memes[meme]['price']
            portfolio_value += value
            st.metric(f"{meme} ({shares} shares)", f"${value:.2f}")
    
    st.metric("Available Cash", f"${st.session_state.cash:.2f}")
    st.metric("Total Portfolio", f"${portfolio_value:.2f}")

# Trading Section
st.subheader("💎 Trading Desk")
trade_col1, trade_col2, trade_col3 = st.columns(3)

with trade_col1:
    selected_meme = st.selectbox("Choose Meme", list(st.session_state.memes.keys()))
    
with trade_col2:
    trade_action = st.radio("Action", ["Buy", "Sell"])
    
with trade_col3:
    quantity = st.number_input("Shares", min_value=1, value=1)

if st.button("Execute Trade", type="primary"):
    if trade_action == "Buy":
        if buy_meme(selected_meme, quantity):
            st.success(f"✅ Bought {quantity} {selected_meme}!")
        else:
            st.error("❌ Not enough cash!")
    else:
        if sell_meme(selected_meme, quantity):
            st.success(f"✅ Sold {quantity} {selected_meme}!")
        else:
            st.error("❌ Not enough shares!")

# Trade History
if st.session_state.trade_history:
    st.subheader("📋 Recent Trades")
    history_df = pd.DataFrame(st.session_state.trade_history[-10:])
    st.dataframe(history_df, use_container_width=True)

# Market Control
st.subheader("🎮 Market Controls")
if st.button("Next Round ⏭️"):
    update_prices_with_real_data()
    st.session_state.round += 1
    st.rerun()

st.markdown(f"**Round:** {st.session_state.round}")

# Auto-refresh every 30 seconds
st.progress(st.session_state.round % 10 / 10)
