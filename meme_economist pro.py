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
        'Dogecoin': {'price': 0.10, 'volatility': 0.3, 'mentions': 0},  # Starting near real price
        'Distracted Boyfriend': {'price': 75.00, 'volatility': 0.15, 'mentions': 0},
        'Pepe the Frog': {'price': 120.00, 'volatility': 0.25, 'mentions': 0},
        'Drake Template': {'price': 80.00, 'volatility': 0.22, 'mentions': 0}
    }
    st.session_state.cash = 10000.00
    st.session_state.portfolio = {meme: 0 for meme in st.session_state.memes}
    st.session_state.trade_history = []
    st.session_state.round = 1
    st.session_state.initialized = True
    st.session_state.premium_clicks = 0

def get_real_dogecoin_price():
    """Get REAL Dogecoin price from CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['dogecoin']['usd']
        else:
            return None
    except:
        return None

def update_prices_with_real_data():
    """Update prices with REAL Dogecoin data + simulated meme data"""
    # Get REAL Dogecoin price
    real_doge_price = get_real_dogecoin_price()
    
    for meme, data in st.session_state.memes.items():
        # SPECIAL CASE: Dogecoin uses REAL price
        if meme == 'Dogecoin' and real_doge_price:
            old_price = data['price']
            new_price = real_doge_price
            change_pct = ((new_price - old_price) / old_price) * 100
            
            st.session_state.memes[meme]['price'] = round(new_price, 4)  # More decimals for crypto
            st.session_state.memes[meme]['change'] = change_pct
            st.session_state.memes[meme]['mentions'] = random.randint(0, 50)
            
        else:
            # Other memes use simulated data
            mentions = random.randint(0, 50)
            mention_effect = min(mentions * 0.001, 0.1)
            volatility_effect = random.uniform(-data['volatility'], data['volatility'])
            total_change = mention_effect + volatility_effect
            
            if random.random() < 0.02:  # 2% chance of viral event
                total_change *= 4
            
            new_price = max(0.01, data['price'] * (1 + total_change))
            st.session_state.memes[meme]['price'] = round(new_price, 2)
            st.session_state.memes[meme]['change'] = total_change * 100
            st.session_state.memes[meme]['mentions'] = mentions

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
st.markdown("**Real-time meme trading powered by LIVE Dogecoin data**")

# Sidebar with real data and monetization
with st.sidebar:
    st.header("🌐 Real Crypto Data")
    
    # Display real Dogecoin price
    real_doge = get_real_dogecoin_price()
    if real_doge:
        st.metric("🐕 Real Dogecoin Price", f"${real_doge:.4f}")
    else:
        st.metric("🐕 Real Dogecoin Price", "Fetching...")
    
    st.caption("Live from CoinGecko API")
    st.markdown("---")
    
    # Business Metrics
    st.header("📊 Business Metrics")
    st.metric("Rounds Played", st.session_state.round)
    st.metric("Total Trades", len(st.session_state.trade_history))
    total_market_cap = sum([data['price'] for data in st.session_state.memes.values()])
    st.metric("Market Cap", f"${total_market_cap:,.0f}")
    
    st.markdown("---")
    
    # Monetization Section
    st.header("💎 Meme Economist Pro")
    st.markdown("**Premium Features:**")
    st.markdown("✅ Real Reddit API data  \n✅ Live Twitter trends  \n✅ Portfolio alerts  \n✅ Advanced charts  \n✅ Priority support")

    # Payment options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Monthly: $5", use_container_width=True):
            st.session_state.premium_clicks += 1
            st.markdown("[**PayPal Subscribe**](https://paypal.com)")
            st.success("Email receipt to: your-email@gmail.com")
    with col2:
        if st.button("💎 Lifetime: $49", use_container_width=True):
            st.session_state.premium_clicks += 1
            st.markdown("[**PayPal One-Time**](https://paypal.com)")
            st.success("Email receipt to: your-email@gmail.com")
    
    st.caption(f"✨ Premium interest: {st.session_state.premium_clicks} clicks")
    
    st.markdown("---")
    st.header("🤝 Sponsor This Project")
    st.markdown("Get your brand in front of meme traders!")
    st.markdown("[**Contact: your-email@gmail.com**](mailto:your-email@gmail.com)")

# Main columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Live Market")
    
    # Market data table
    market_data = []
    for meme, data in st.session_state.memes.items():
        change = data.get('change', 0)
        change_icon = "🟢" if change > 0 else "🔴"
        
        # Show more decimals for Dogecoin
        price_format = f"${data['price']:.4f}" if meme == 'Dogecoin' else f"${data['price']:.2f}"
        
        market_data.append({
            'Meme': meme,
            'Price': price_format,
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

# Premium Features Teaser
st.markdown("---")
st.header("🚀 Premium Features - Coming Soon!")

premium_col1, premium_col2, premium_col3 = st.columns(3)

with premium_col1:
    st.subheader("📊 Real Data")
    st.markdown("""
    - Live Reddit mentions
    - Twitter sentiment analysis  
    - Google Trends integration
    - Real-time meme virality scores
    """)

with premium_col2:
    st.subheader("🎯 Advanced Tools")
    st.markdown("""
    - Portfolio performance analytics
    - Price prediction algorithms
    - Custom meme tracking
    - Export to CSV/Excel
    """)

with premium_col3:
    st.subheader("🔔 Smart Alerts")
    st.markdown("""
    - Price movement notifications
    - Virality spike detection
    - Competitor tracking
    - Discord/Telegram bots
    """)

# Market Control
st.subheader("🎮 Market Controls")
if st.button("Next Round ⏭️"):
    update_prices_with_real_data()
    st.session_state.round += 1
    st.rerun()

st.markdown(f"**Round:** {st.session_state.round}")

# Auto-refresh every 30 seconds
st.progress(st.session_state.round % 10 / 10)

