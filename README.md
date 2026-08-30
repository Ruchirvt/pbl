# 🌤️ SkyCast AI — Creative Weather Prediction Website

A stunning, AI-powered weather prediction web application built with **Streamlit** and **Python**. Features real-time weather data, 7-day forecasts, interactive charts, and trend-based predictions — all wrapped in a beautiful glassmorphism UI.

![SkyCast AI](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Open-Meteo](https://img.shields.io/badge/Open--Meteo-API-blue?style=for-the-badge)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌍 **Real-Time Weather** | Live weather data for any city worldwide |
| 📅 **7-Day Forecast** | Detailed daily forecasts with weather icons |
| 🔮 **AI Predictions** | Trend-based predictions for the next 3 days |
| 📊 **Interactive Charts** | Temperature trends & precipitation probability |
| 🎨 **Glassmorphism UI** | Modern, animated, responsive design |
| 💧 **Weather Metrics** | Humidity, wind speed, pressure, feels-like temp |
| 🆓 **No API Key Needed** | Uses free Open-Meteo API |

---

## 🚀 Quick Start (Local)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/skycast-ai.git
cd skycast-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🌐 Deploy to Streamlit Cloud (Free Hosting)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - SkyCast AI"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/skycast-ai.git
git push -u origin main
```

### Step 2: Deploy
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository: `YOUR_USERNAME/skycast-ai`
5. Set **Main file path** to `app.py`
6. Click **Deploy!** 🚀

Your app will be live at: `https://skycast-ai-xxx.streamlit.app`

---

## 📁 Project Structure

```
skycast-ai/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .streamlit/
    └── config.toml        # Streamlit theme configuration
```

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit + Custom CSS (Glassmorphism)
- **Charts**: Plotly Express & Graph Objects
- **Data**: Pandas
- **API**: Open-Meteo (Free, no key required)
- **Icons**: Unicode Emoji
- **Animations**: CSS Keyframes

---

## 🎨 UI Highlights

- **Gradient Backgrounds**: Deep purple space theme
- **Glass Cards**: `backdrop-filter: blur(20px)`
- **Hover Effects**: Cards lift and glow on hover
- **Floating Animation**: Gentle up-down motion on main card
- **Responsive Grid**: Adapts to all screen sizes
- **Dynamic Charts**: Dark-themed Plotly visualizations

---

## 🔮 How Predictions Work

The AI prediction feature analyzes temperature trends from the 7-day forecast:

1. Calculates the slope of max/min temperature changes
2. Extrapolates the trend for the next 3 days
3. Shows trend direction (warming ↗️ / cooling ↘️ / stable ➡️)

> **Note**: This is a simplified trend-based model. For production ML predictions, integrate TensorFlow/PyTorch models with historical weather data.

---

## 📝 Customization Ideas

Want to make it even cooler? Try these:

- [ ] Add **OpenWeatherMap API** for more detailed data (requires free API key)
- [ ] Integrate **machine learning** with scikit-learn for better predictions
- [ ] Add **weather maps** using Folium or PyDeck
- [ ] Include **sunrise/sunset** times with animated sun/moon
- [ ] Add **severe weather alerts** section
- [ ] Create **city comparison** feature
- [ ] Add **historical weather data** charts
- [ ] Implement **user favorites** with session state

---

## 📄 License

MIT License — feel free to use, modify, and deploy!

---

## 🙌 Credits

- Weather data: [Open-Meteo API](https://open-meteo.com/)
- Built with: [Streamlit](https://streamlit.io/)
- Icons: Unicode Emoji

---

<div align="center">
  <h3>⭐ Star this repo if you found it helpful!</h3>
  <p>Made with 💜 and Python</p>
</div>
