import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime

# 🌐 Page setup
st.set_page_config(page_title="🌦 Weather App", page_icon="🌦", layout="centered")

# 🎨 Title block
st.markdown("""
    <h1 style='text-align: center;'>🌦 Weather App</h1>
    <h3 style='text-align: center; color: #4b6cb7;'>by Mehreen</h3>
    <p style='text-align: center;'>Get real-time weather updates with location maps and country flags</p>
""", unsafe_allow_html=True)

# 📥 City input
city = st.text_input("🌍 Enter City Name")
API_KEY = "8422d0579f796c2c6558875825314c6a"  # 🔑 Replace this with your actual OpenWeatherMap API key

if city:
    try:
        # 📍 Geolocation API call
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_response = requests.get(geo_url).json()

        if not geo_response:
            st.error("❌ City not found. Please try again.")
        else:
            location = geo_response[0]
            lat = location["lat"]
            lon = location["lon"]
            city_name = location["name"]
            country_code = location["country"]

            # 🏳️ Country flag
            flag_url = f"https://flagsapi.com/{country_code}/flat/64.png"
            st.image(flag_url, width=64)

            # 🌦 Weather API call
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            weather_data = requests.get(weather_url).json()

            if weather_data.get("cod") != 200:
                st.error("⚠️ Weather data not available.")
            else:
                # 🌞 Format sunrise/sunset times
                sunrise_ts = weather_data["sys"]["sunrise"]
                sunset_ts = weather_data["sys"]["sunset"]
                sunrise = datetime.fromtimestamp(sunrise_ts).strftime('%I:%M %p')
                sunset = datetime.fromtimestamp(sunset_ts).strftime('%I:%M %p')

                # 🌡️ Weather details
                temp = weather_data["main"]["temp"]
                feels_like = weather_data["main"]["feels_like"]
                weather_desc = weather_data["weather"][0]["description"].title()
                humidity = weather_data["main"]["humidity"]
                wind = weather_data["wind"]["speed"]

                # 📊 Display block
                st.markdown(f"### 📍 Weather in {city_name}, {country_code}")
                st.markdown(f"**🌤 Condition:** {weather_desc}")
                st.markdown(f"**🌡 Temperature:** {temp}°C")
                st.markdown(f"**🥵 Feels Like:** {feels_like}°C")
                
                if abs(temp - feels_like) > 1:
                    diff = round(feels_like - temp, 1)
                    note = "warmer" if diff > 0 else "cooler"
                    st.markdown(f"🧠 *Feels {note} than actual by {abs(diff)}°C*")

                st.markdown(f"**💧 Humidity:** {humidity}%")
                st.markdown(f"**💨 Wind Speed:** {wind} m/s")
                st.markdown(f"**🌅 Sunrise:** {sunrise}")
                st.markdown(f"**🌇 Sunset:** {sunset}")
                st.markdown(f"**📍 Coordinates:** `{lat}, {lon}`")

                # 🗺️ Location map
                st.markdown("### 🗺 Map View:")
                map = folium.Map(location=[lat, lon], zoom_start=10)
                folium.Marker([lat, lon], popup=city_name).add_to(map)
                st_folium(map, width=700)

    except Exception as e:
        st.error(f"🚨 Error: {e}

                            









