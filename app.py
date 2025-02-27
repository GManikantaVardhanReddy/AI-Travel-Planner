import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from streamlit_lottie import st_lottie
import requests
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from datetime import datetime
import os
import json
from io import StringIO
import openmeteo_requests
import pandas as pd

# Configuration and Initialization
def initialize_app():
    try:
        api_key = os.getenv("AIzaSyDplai8TdzRpuYaY73_cRD0JiZajCyhq") or "AIzaSyDplai8TdzRpuYaY73_cRD0JiZajCyhqu"
        genai = ChatGoogleGenerativeAI(api_key=api_key, model='gemini-1.5-flash')
        return genai
    except Exception as e:
        st.error(f"Failed to initialize AI model: {e}")
        return None

# Utility Functions
def load_lottieurl(url: str) -> dict:
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        st.warning(f"Failed to load animation: {e}")
        return {}

def get_coordinates(place: str) -> tuple:
    try:
        geolocator = Nominatim(user_agent="travel_planner")
        location = geolocator.geocode(place, timeout=10)
        return (location.latitude, location.longitude) if location else (None, None)
    except GeocoderTimedOut:
        st.warning(f"Geocoding timed out for {place}")
        return None, None
    except GeocoderUnavailable:
        st.warning(f"Geocoding service unavailable for {place}")
        return None, None
    except AttributeError:
        st.warning(f"Invalid location data for {place}")
        return None, None

def get_weather(lat: float, lon: float, date: datetime) -> dict:
    try:
        client = openmeteo_requests.Client()
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_max", "temperature_2m_min", "weathercode"],
            "timezone": "auto",
            "start_date": date.strftime('%Y-%m-%d'),
            "end_date": date.strftime('%Y-%m-%d')
        }
        response = client.weather_api(url, params=params)[0].daily()
        return {
            "max_temp": response.variables(0).values()[0],
            "min_temp": response.variables(1).values()[0],
            "weather_code": response.variables(2).values()[0]
        }
    except Exception as e:
        st.warning(f"Could not fetch weather data: {e}")
        return {
            "max_temp": 0.0,
            "min_temp": 0.0,
            "weather_code": -1
        }

# Static currency exchange rates to USD (approximate as of Feb 2025)
# For real-time rates, use an API like exchangerate-api.com
CURRENCY_RATES = {
    "INR": 83.0,  # Indian Rupee
    "EUR": 0.94,  # Euro
    "GBP": 0.80,  # British Pound
    "JPY": 150.0, # Japanese Yen
    "CAD": 1.35,  # Canadian Dollar
    "AUD": 1.50,  # Australian Dollar
    "CHF": 0.90,  # Swiss Franc
    "CNY": 7.10,  # Chinese Yuan
    "USD": 1.0,   # U.S. Dollar (base currency)
    # Add more currencies as needed
}

# Convert any currency to USD
def to_usd(amount: float, currency: str) -> float:
    if currency not in CURRENCY_RATES:
        return amount  # Default to no conversion if currency not found
    return amount / CURRENCY_RATES[currency]

# Main App
def main():
    st.set_page_config(
        page_title="AI Travel Planner Pro",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main { background-color: #f0f4f8; padding: 20px; }
        .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; padding: 0.5em 1em; }
        .stTextInput>div>input, .stDateInput>div>input, .stSelectbox>div>select {
            border-radius: 8px; border: 1px solid #ced4da;
        }
        .weather-box { background-color: #e3f2fd; padding: 10px; border-radius: 5px; }
        </style>
    """, unsafe_allow_html=True)

    # Initialize AI
    genai = initialize_app()
    if not genai:
        return

    # Sidebar
    with st.sidebar:
        st.header("Travel Planner Pro")
        st.info("Enhanced AI-powered travel planning with weather and multi-currency budget features")
        lottie_data = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_u4yrau.json")
        if lottie_data:
            st_lottie(lottie_data, height=150, key="travel_anim")

    # Main Content
    st.title("🌍 Travel Planner Pro")
    st.subheader("Your ultimate travel companion")

    # Input Form
    with st.form(key='travel_form'):
        col1, col2 = st.columns(2)
        with col1:
            source = st.text_input("Starting Point", placeholder="e.g., New York")
            travel_date = st.date_input("Travel Date", min_value=datetime.today())
            budget = st.number_input("Budget", min_value=0, value=500)
            currency = st.selectbox("Currency", options=list(CURRENCY_RATES.keys()), index=0)  # Default to INR
            budget_usd = to_usd(budget, currency)  # Convert to USD for internal use
            st.write(f"Equivalent in USD: ${budget_usd:,.2f}")
        with col2:
            destination = st.text_input("Destination", placeholder="e.g., London")
            duration = st.number_input("Trip Duration (days)", min_value=1, value=1)
            travel_modes = ["Any", "Flight", "Train", "Bus", "Car"]
            preference = st.selectbox("Preferred Transport", travel_modes)

        submit = st.form_submit_button("Plan My Trip")

    # Process Submission
    if submit:
        if not all([source, destination]):
            st.error("Please fill in both starting point and destination")
            return

        with st.spinner("Planning your trip..."):
            # AI Query (using USD internally for consistency with most travel data)
            query = (
                f"Plan a detailed trip from {source} to {destination} "
                f"starting on {travel_date.strftime('%Y-%m-%d')} for {duration} days. "
                f"Include travel options ({', '.join(travel_modes[1:])}), "
                f"accommodation suggestions (within ${budget_usd:.2f} total budget in USD), "
                f"top attractions with estimated costs, and daily itinerary. "
                f"Preferred transport: {preference}"
            )

            try:
                response = genai.invoke(query)
                itinerary = response.content

                # Display Results
                st.markdown("### Your Travel Itinerary")
                st.write(itinerary)
                st.write(f"**Total Budget:** {budget:,.2f} {currency} (≈ ${budget_usd:,.2f})")

                # Weather Information
                dest_coords = get_coordinates(destination)
                if dest_coords and None not in dest_coords:
                    weather = get_weather(dest_coords[0], dest_coords[1], travel_date)
                    st.markdown("### Weather Forecast")
                    if weather["weather_code"] != -1:
                        st.markdown(
                            f'<div class="weather-box">'
                            f'📅 {travel_date.strftime("%B %d, %Y")}<br>'
                            f'🌡️ Max: {weather["max_temp"]:.1f}°C | Min: {weather["min_temp"]:.1f}°C'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.info("Weather information unavailable")

                # Map Visualization
                source_coords = get_coordinates(source)
                if None in source_coords + dest_coords:
                    st.warning("Could not generate map due to location lookup failure")
                else:
                    map_data = [
                        {"name": source, "lat": source_coords[0], "lon": source_coords[1]},
                        {"name": destination, "lat": dest_coords[0], "lon": dest_coords[1]}
                    ]

                    layers = [
                        pdk.Layer(
                            'ScatterplotLayer',
                            data=map_data,
                            get_position='[lon, lat]',
                            get_color='[200, 30, 0, 160]',
                            get_radius=50000,
                            pickable=True
                        ),
                        pdk.Layer(
                            'PathLayer',
                            data=[{"path": [[source_coords[1], source_coords[0]],
                                          [dest_coords[1], dest_coords[0]]]}],
                            get_path="path",
                            get_width=1000,
                            get_color='[100, 100, 100, 100]',
                            width_min_pixels=2
                        )
                    ]

                    st.pydeck_chart(pdk.Deck(
                        layers=layers,
                        initial_view_state=pdk.ViewState(
                            latitude=sum(p["lat"] for p in map_data) / 2,
                            longitude=sum(p["lon"] for p in map_data) / 2,
                            zoom=4,
                            pitch=45
                        ),
                        tooltip={"text": "{name}"}
                    ))

                # Save Itinerary
                itinerary_data = {
                    "source": source,
                    "destination": destination,
                    "date": travel_date.strftime('%Y-%m-%d'),
                    "duration": duration,
                    "budget": budget,
                    "currency": currency,
                    "budget_usd": budget_usd,
                    "preference": preference,
                    "itinerary": itinerary
                }
                st.download_button(
                    label="Download Itinerary",
                    data=json.dumps(itinerary_data, indent=2),
                    file_name=f"trip_{source}_to_{destination}.json",
                    mime="application/json"
                )

            except Exception as e:
                st.error(f"Error generating travel plan: {e}")

    st.markdown("---")
    st.caption("© 2025 Travel Planner Pro")

if __name__ == "__main__":
    main()
