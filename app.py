from flask import Flask, render_template
import weather_api

app = Flask(__name__)

@app.route('/')
def home():
    # Logic to fetch weather data and pass it to the template
    # Render the home template and pass the weather data to it
    weather_data = weather_api.fetch_hourly_weather_data()

    # Mapping from weather type codes to names and icon class names
    weather_icon_map = {
        "0": {"name": "Clear night", "icon": "fas fa-moon"},
        "1": {"name": "Sunny day", "icon": "fas fa-sun"},
        "2": {"name": "Partly cloudy (night)", "icon": "fas fa-cloud-moon"},
        "3": {"name": "Partly cloudy (day)", "icon": "fas fa-cloud-sun"},
        "5": {"name": "Mist", "icon": "fas fa-smog"},
        "6": {"name": "Fog", "icon": "fas fa-smog"},
        "7": {"name": "Cloudy", "icon": "fas fa-cloud"},
        "8": {"name": "Overcast", "icon": "fas fa-cloud"},
        "9": {"name": "Light rain shower (night)", "icon": "fas fa-cloud-showers-heavy"},
        "10": {"name": "Light rain shower (day)", "icon": "fas fa-cloud-sun-rain"},
        "11": {"name": "Drizzle", "icon": "fas fa-cloud-rain"},
        "12": {"name": "Light rain", "icon": "fas fa-cloud-rain"},
        "13": {"name": "Heavy rain shower (night)", "icon": "fas fa-cloud-showers-heavy"},
        "14": {"name": "Heavy rain shower (day)", "icon": "fas fa-cloud-sun-rain"},
        "15": {"name": "Heavy rain", "icon": "fas fa-cloud-showers-heavy"},
        "16": {"name": "Sleet shower (night)", "icon": "fas fa-cloud-moon-rain"},
        "17": {"name": "Sleet shower (day)", "icon": "fas fa-cloud-sun-rain"},
        "18": {"name": "Sleet", "icon": "fas fa-snowflake"},
        "19": {"name": "Hail shower (night)", "icon": "fas fa-cloud-moon-rain"},
        "20": {"name": "Hail shower (day)", "icon": "fas fa-cloud-sun-rain"},
        "21": {"name": "Hail", "icon": "fas fa-snowflake"},
        "22": {"name": "Light snow shower (night)", "icon": "fas fa-snowflake"},
        "23": {"name": "Light snow shower (day)", "icon": "fas fa-snowflake"},
        "24": {"name": "Light snow", "icon": "fas fa-snowflake"},
        "25": {"name": "Heavy snow shower (night)", "icon": "fas fa-snowflake"},
        "26": {"name": "Heavy snow shower (day)", "icon": "fas fa-snowflake"},
        "27": {"name": "Heavy snow", "icon": "fas fa-snowflake"},
        "28": {"name": "Thunder shower (night)", "icon": "fas fa-bolt"},
        "29": {"name": "Thunder shower (day)", "icon": "fas fa-bolt"},
        "30": {"name": "Thunder", "icon": "fas fa-bolt"}}
    return render_template('home.html', weather_data=weather_data, weather_icon_map=weather_icon_map)

               


@app.route('/filter', methods=['GET', 'POST'])
def filter():
    # Logic to handle form submission and filtering of weather data
    # Render the filter template with the filtered weather data
    filtered_data = 0
    return render_template('filter.html', filtered_data=filtered_data)

@app.route('/event-planning', methods=['GET', 'POST'])
def event_planning():
    # Logic to handle event planning and note-taking
    # Render the event planning template with the event data
    event_data=0
    return render_template('event_planning.html', event_data=event_data)

@app.route('/setting', methods=['GET', 'POST'])
def settle():
    # Logic to handle GPS opening/closing
    # Render the settle template
    return render_template('setting.html')
