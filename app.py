import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="SkyCast AI | Weather Prediction",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    * { font-family: 'Outfit', sans-serif; }

    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }

    .weather-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    .weather-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.2);
    }

    .temp-display {
        font-size: 6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #ffd89b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }

    .city-name {
        font-size: 2.5rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.5rem;
    }

    .weather-desc {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.7);
        text-transform: capitalize;
    }

    .metric-box {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
    }

    .metric-label {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 0.2rem;
    }

    .forecast-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }

    .forecast-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: scale(1.05);
    }

    .forecast-day {
        font-size: 1rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 0.5rem;
    }

    .forecast-icon {
        font-size: 2.5rem;
        margin: 0.5rem 0;
    }

    .forecast-temp {
        font-size: 1.3rem;
        font-weight: 700;
        color: white;
    }

    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 1rem 1.5rem !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 16px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    }

    .prediction-badge {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 1rem;
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .trend-up { color: #38ef7d; }
    .trend-down { color: #f5576c; }

    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 24px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Animated background particles */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    .floating {
        animation: float 6s ease-in-out infinite;
    }

    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== WEATHER ICONS ====================
WEATHER_ICONS = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '❄️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Haze': '🌫️',
    'Smoke': '🌫️',
    'Dust': '🌫️',
    'Sand': '🌫️',
    'Tornado': '🌪️',
    'Squall': '💨'
}

# ==================== API CONFIG ====================
# Using Open-Meteo API (free, no key needed) for demo
# For production, replace with OpenWeatherMap API key

def get_weather_data(city):
    """Fetch weather data from Open-Meteo API (free, no key)"""
    try:
        # First, geocode the city
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response = requests.get(geo_url, timeout=10)
        geo_data = geo_response.json()

        if 'results' not in geo_data or not geo_data['results']:
            return None, "City not found. Please try another city name."

        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']
        city_name = geo_data['results'][0]['name']
        country = geo_data['results'][0].get('country', '')

        # Fetch current weather + 7-day forecast
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,surface_pressure,visibility&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max&timezone=auto&forecast_days=8"

        weather_response = requests.get(weather_url, timeout=10)
        weather_data = weather_response.json()

        return {
            'city': city_name,
            'country': country,
            'current': weather_data['current'],
            'daily': weather_data['daily']
        }, None

    except Exception as e:
        return None, f"Error fetching weather data: {str(e)}"

def get_weather_description(code):
    """Convert WMO weather code to description and icon"""
    codes = {
        0: ('Clear', '☀️'),
        1: ('Clear', '🌤️'), 2: ('Clouds', '⛅'), 3: ('Clouds', '☁️'),
        45: ('Fog', '🌫️'), 48: ('Fog', '🌫️'),
        51: ('Drizzle', '🌦️'), 53: ('Drizzle', '🌦️'), 55: ('Drizzle', '🌧️'),
        56: ('Drizzle', '🌧️'), 57: ('Drizzle', '🌧️'),
        61: ('Rain', '🌧️'), 63: ('Rain', '🌧️'), 65: ('Rain', '🌧️'),
        66: ('Rain', '🌧️'), 67: ('Rain', '🌧️'),
        71: ('Snow', '🌨️'), 73: ('Snow', '🌨️'), 75: ('Snow', '❄️'),
        77: ('Snow', '❄️'),
        80: ('Rain', '🌧️'), 81: ('Rain', '🌧️'), 82: ('Rain', '⛈️'),
        85: ('Snow', '🌨️'), 86: ('Snow', '❄️'),
        95: ('Thunderstorm', '⛈️'), 96: ('Thunderstorm', '⛈️'), 99: ('Thunderstorm', '🌪️')
    }
    return codes.get(code, ('Clear', '☀️'))

def predict_next_days(daily_data):
    """Simple prediction model based on trend analysis"""
    temps_max = daily_data['temperature_2m_max']
    temps_min = daily_data['temperature_2m_min']

    # Calculate trend
    if len(temps_max) >= 3:
        trend_max = (temps_max[-1] - temps_max[0]) / len(temps_max)
        trend_min = (temps_min[-1] - temps_min[0]) / len(temps_min)
    else:
        trend_max = 0
        trend_min = 0

    predictions = []
    for i in range(1, 4):  # Predict next 3 days
        pred_max = temps_max[-1] + (trend_max * i)
        pred_min = temps_min[-1] + (trend_min * i)
        predictions.append({
            'day': (datetime.now() + timedelta(days=7+i)).strftime('%a'),
            'date': (datetime.now() + timedelta(days=7+i)).strftime('%b %d'),
            'max_temp': round(pred_max, 1),
            'min_temp': round(pred_min, 1),
            'trend': 'warming' if trend_max > 0.5 else 'cooling' if trend_max < -0.5 else 'stable'
        })

    return predictions

# ==================== MAIN UI ====================
st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3.5rem; font-weight: 800; color: white; margin-bottom: 0.5rem;">
            🌤️ SkyCast AI
        </h1>
        <p style="font-size: 1.2rem; color: rgba(255,255,255,0.6); margin-bottom: 2rem;">
            Intelligent Weather Prediction & Forecasting
        </p>
    </div>
""", unsafe_allow_html=True)

# Search bar
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    city = st.text_input("", placeholder="Enter city name...", value="London", key="city_input")
    search_clicked = st.button("🔍 Search", use_container_width=True)

# Default city or search
if search_clicked or city:
    with st.spinner("🌐 Fetching weather data..."):
        data, error = get_weather_data(city)

    if error:
        st.error(error)
    elif data:
        current = data['current']
        daily = data['daily']

        # Get weather description
        weather_desc, weather_icon = get_weather_description(current.get('weather_code', 0))

        # ==================== CURRENT WEATHER ====================
        st.markdown("<div class='section-title'>📍 Current Conditions</div>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f"""
                <div class="weather-card floating">
                    <div class="city-name">{data['city']}, {data['country']}</div>
                    <div style="display: flex; align-items: center; gap: 1rem; margin: 1rem 0;">
                        <span style="font-size: 4rem;">{weather_icon}</span>
                        <div>
                            <div class="temp-display">{round(current['temperature_2m'])}°</div>
                            <div class="weather-desc">{weather_desc}</div>
                        </div>
                    </div>
                    <div class="prediction-badge">✨ AI-Powered Forecast Active</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='weather-card'>", unsafe_allow_html=True)

            # Metrics grid
            mcol1, mcol2 = st.columns(2)
            with mcol1:
                st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-icon">💧</div>
                        <div class="metric-value">{current['relative_humidity_2m']}%</div>
                        <div class="metric-label">Humidity</div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="metric-box" style="margin-top: 1rem;">
                        <div class="metric-icon">💨</div>
                        <div class="metric-value">{current['wind_speed_10m']} km/h</div>
                        <div class="metric-label">Wind Speed</div>
                    </div>
                """, unsafe_allow_html=True)

            with mcol2:
                st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-icon">🌡️</div>
                        <div class="metric-value">{round(current['apparent_temperature'])}°</div>
                        <div class="metric-label">Feels Like</div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="metric-box" style="margin-top: 1rem;">
                        <div class="metric-icon">📊</div>
                        <div class="metric-value">{current['surface_pressure']} hPa</div>
                        <div class="metric-label">Pressure</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ==================== 7-DAY FORECAST ====================
        st.markdown("<div class='section-title'>📅 7-Day Forecast</div>", unsafe_allow_html=True)

        forecast_cols = st.columns(7)
        for i in range(7):
            day_date = daily['time'][i]
            day_name = datetime.strptime(day_date, '%Y-%m-%d').strftime('%a')
            date_str = datetime.strptime(day_date, '%Y-%m-%d').strftime('%b %d')
            max_temp = daily['temperature_2m_max'][i]
            min_temp = daily['temperature_2m_min'][i]
            weather_code = daily['weather_code'][i]
            _, icon = get_weather_description(weather_code)
            precip_prob = daily['precipitation_probability_max'][i]

            with forecast_cols[i]:
                st.markdown(f"""
                    <div class="forecast-card">
                        <div class="forecast-day">{day_name}</div>
                        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">{date_str}</div>
                        <div class="forecast-icon">{icon}</div>
                        <div class="forecast-temp">{round(max_temp)}°</div>
                        <div style="font-size: 0.9rem; color: rgba(255,255,255,0.5);">{round(min_temp)}°</div>
                        <div style="font-size: 0.75rem; color: #667eea; margin-top: 0.3rem;">💧 {precip_prob}%</div>
                    </div>
                """, unsafe_allow_html=True)

        # ==================== TEMPERATURE TREND CHART ====================
        st.markdown("<div class='section-title'>📈 Temperature Trends</div>", unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns([2, 1])

        with chart_col1:
            # Prepare data for chart
            df = pd.DataFrame({
                'Day': [datetime.strptime(d, '%Y-%m-%d').strftime('%a %d') for d in daily['time']],
                'Max Temp': daily['temperature_2m_max'],
                'Min Temp': daily['temperature_2m_min'],
                'Avg Temp': [(max_t + min_t) / 2 for max_t, min_t in zip(daily['temperature_2m_max'], daily['temperature_2m_min'])]
            })

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df['Day'], y=df['Max Temp'],
                mode='lines+markers',
                name='High',
                line=dict(color='#f5576c', width=3),
                marker=dict(size=8, symbol='circle'),
                fill='tonexty',
                fillcolor='rgba(245, 87, 108, 0.1)'
            ))

            fig.add_trace(go.Scatter(
                x=df['Day'], y=df['Min Temp'],
                mode='lines+markers',
                name='Low',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8, symbol='circle'),
                fill='tonexty',
                fillcolor='rgba(102, 126, 234, 0.1)'
            ))

            fig.add_trace(go.Scatter(
                x=df['Day'], y=df['Avg Temp'],
                mode='lines',
                name='Average',
                line=dict(color='#38ef7d', width=2, dash='dash'),
            ))

            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Outfit'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                margin=dict(l=20, r=20, t=60, b=20),
                height=400,
                xaxis=dict(showgrid=False, color='rgba(255,255,255,0.5)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)')
            )

            st.plotly_chart(fig, use_container_width=True)

        with chart_col2:
            # AI Prediction section
            predictions = predict_next_days(daily)

            st.markdown("""
                <div class="weather-card" style="height: 400px;">
                    <h3 style="color: white; margin-bottom: 1rem;">🔮 AI Predictions</h3>
                    <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-bottom: 1.5rem;">
                        Next 3 days forecast based on trend analysis
                    </p>
            """, unsafe_allow_html=True)

            for pred in predictions:
                trend_icon = '📈' if pred['trend'] == 'warming' else '📉' if pred['trend'] == 'cooling' else '➡️'
                trend_color = '#38ef7d' if pred['trend'] == 'warming' else '#f5576c' if pred['trend'] == 'cooling' else '#ffd89b'

                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem; border: 1px solid rgba(255,255,255,0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="color: white; font-weight: 600;">{pred['day']}, {pred['date']}</div>
                                <div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">High: {pred['max_temp']}° | Low: {pred['min_temp']}°</div>
                            </div>
                            <div style="color: {trend_color}; font-size: 1.2rem;">{trend_icon}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ==================== PRECIPITATION CHART ====================
        st.markdown("<div class='section-title'>🌧️ Precipitation Probability</div>", unsafe_allow_html=True)

        precip_df = pd.DataFrame({
            'Day': [datetime.strptime(d, '%Y-%m-%d').strftime('%a') for d in daily['time']],
            'Probability': daily['precipitation_probability_max']
        })

        fig_precip = px.bar(
            precip_df, x='Day', y='Probability',
            color='Probability',
            color_continuous_scale=['#38ef7d', '#ffd89b', '#f5576c'],
            template='plotly_dark'
        )
        fig_precip.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Outfit'),
            margin=dict(l=20, r=20, t=20, b=20),
            height=300,
            showlegend=False,
            coloraxis_showscale=False
        )
        fig_precip.update_xaxes(showgrid=False, color='rgba(255,255,255,0.5)')
        fig_precip.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)', title='%')

        st.plotly_chart(fig_precip, use_container_width=True)

        # ==================== FOOTER ====================
        st.markdown("""
            <div style="text-align: center; padding: 3rem 0 1rem 0; color: rgba(255,255,255,0.3); font-size: 0.9rem;">
                <p>🌤️ SkyCast AI | Powered by Open-Meteo API | Built with Streamlit</p>
                <p style="font-size: 0.8rem;">Data provided for educational purposes. Predictions use simple trend analysis.</p>
            </div>
        """, unsafe_allow_html=True)

else:
    # Initial state
    st.markdown("""
        <div style="text-align: center; padding: 4rem 0; color: rgba(255,255,255,0.4);">
            <div style="font-size: 5rem; margin-bottom: 1rem;">🌍</div>
            <h2 style="color: rgba(255,255,255,0.6); font-weight: 400;">Enter a city name above to get started</h2>
            <p style="margin-top: 1rem;">Get real-time weather data, 7-day forecasts, and AI-powered predictions</p>
        </div>
    """, unsafe_allow_html=True)
