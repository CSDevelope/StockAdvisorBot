# ai_response.py

import google.generativeai as genai
from data_acquisition import fetch_stock_data
from pattern_recognition import calculate_indicators
from trading_recommendations import generate_signals
import os

def configure_ai(api_key):
    genai.configure(api_key=api_key)

def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

def handle_stock_analysis(symbol):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    data = fetch_stock_data(symbol, api_key)
    data = calculate_indicators(data)
    data = generate_signals(data)
    return data

def get_stock_recommendation(symbol):
    data = handle_stock_analysis(symbol)
    if data['Signal'].iloc[-1] == 1:
        return "Recommendation: Buy Call"
    elif data['Signal'].iloc[-1] == -1:
        return "Recommendation: Buy Put"
    else:
        return "Recommendation: Hold"
