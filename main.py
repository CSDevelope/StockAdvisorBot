# main.py

from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import logging
from ai_response import configure_ai, get_gemini_response
from data_acquisition import fetch_stock_data
from pattern_recognition import calculate_indicators
from trading_recommendations import generate_signals
from stock_list import get_stock_list
from sentiment_analysis import get_news_sentiment
from market_data import fetch_index_data, get_index_summary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API keys from environment variables
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# Configure AI
configure_ai(os.getenv("GOOGLE_API_KEY"))

# Initialize Streamlit app
st.set_page_config(page_title="Dispersal AI")

st.header("WWW.Dispersal.net AI Preview")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def get_help_message():
    help_message = """
    ### Help Guide
    
    **Stock Analysis**:
    - "Analyze stock SYMBOL" - Get a recommendation for a specific stock. Replace SYMBOL with the stock ticker (e.g., AAPL, MSFT).
    
    **Stock Recommendations for Monday**:
    - "Recommend stocks for Monday" - Get recommendations for all stocks listed in `stock_list.py` for the upcoming Monday.
    
    **Market Summary**:
    - "Market summary" - Get a summary of the market performance for major indices.
    
    **Other Commands**:
    - "Help me" - Display this help guide.
    """
    return help_message

def process_input(user_input):
    if user_input.lower().startswith("analyze stock "):
        symbol = user_input.split(" ")[-1].upper()
        return get_stock_recommendation(symbol)
    elif user_input.lower() == "recommend stocks for monday":
        return recommend_stocks()
    elif user_input.lower() == "market summary":
        return get_market_summary()
    elif user_input.lower() == "help me":
        return get_help_message()
    else:
        return "I'm sorry, I don't understand that command. Type 'help me' for a list of commands."

def recommend_stocks():
    stock_list = get_stock_list()
    recommendations = []

    for symbol in stock_list:
        try:
            data = fetch_stock_data(symbol, alpha_vantage_api_key)
            if data is None or data.empty:
                logger.error(f"No data fetched for {symbol}")
                recommendations.append(f"No data fetched for {symbol}")
                continue
            
            data = calculate_indicators(data)
            data = generate_signals(data)
            sentiments = get_news_sentiment(symbol)
            
            sentiment_score = sum(sentiment['compound'] for sentiment in sentiments) / len(sentiments) if sentiments else 0

            logger.info(f"Symbol: {symbol}, Last Signal: {data['Signal'].iloc[-1]}, Sentiment Score: {sentiment_score}")

            if data['Signal'].iloc[-1] == 1 and sentiment_score > 0:
                recommendations.append(f"Buy Call on {symbol}")
            elif data['Signal'].iloc[-1] == -1 and sentiment_score < 0:
                recommendations.append(f"Buy Put on {symbol}")
            else:
                recommendations.append(f"Hold on {symbol}")
        except Exception as e:
            logger.error(f"Error processing {symbol}: {e}")
            recommendations.append(f"Error processing {symbol}")

    return "\n".join(recommendations)

def get_stock_recommendation(symbol):
    data = fetch_stock_data(symbol, alpha_vantage_api_key)
    if data is None or data.empty:
        logger.error(f"No data fetched for {symbol}")
        return f"No data fetched for {symbol}"

    data = calculate_indicators(data)
    logger.info(f"Data with indicators for {symbol}: {data.tail()}")
    
    data = generate_signals(data)
    logger.info(f"Data with signals for {symbol}: {data.tail()}")
    
    sentiment_score = 0  # Default sentiment score for debugging
    sentiments = get_news_sentiment(symbol)
    if sentiments:
        sentiment_score = sum(sentiment['compound'] for sentiment in sentiments) / len(sentiments)
    
    logger.info(f"Symbol: {symbol}, Last Signal: {data['Signal'].iloc[-1]}, Sentiment Score: {sentiment_score}")

    if data['Signal'].iloc[-1] == 1:
        return f"Recommendation: Buy Call on {symbol}"
    elif data['Signal'].iloc[-1] == -1:
        return f"Recommendation: Buy Put on {symbol}"
    else:
        return f"Recommendation: Hold on {symbol}"

def get_market_summary():
    summary = get_index_summary()
    if summary:
        return "\n".join(summary)
    else:
        return "No market summary data available."

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    bot_response = process_input(input)
    st.write(bot_response)
    st.session_state['chat_history'].append(("Bot", bot_response))
    st.session_state['chat_history'].append(("You", input))

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
