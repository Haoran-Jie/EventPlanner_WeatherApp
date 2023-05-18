from flask import Flask, render_template,request,jsonify, redirect
import weather_api, notification_api

app = Flask(__name__)


# Mapping from weather type codes to names and icon class names
weather_icon_map = {
    "0": {"name": "Clear night", "icon": "fas fa-moon text-blue"},
    "1": {"name": "Sunny day", "icon": "fas fa-sun text-yellow"},
    "2": {"name": "Partly cloudy (night)", "icon": "fas fa-cloud-moon text-blue"},
    "3": {"name": "Partly cloudy (day)", "icon": "fas fa-cloud-sun text-yellow"},
    "5": {"name": "Mist", "icon": "fas fa-smog text-gray"},
    "6": {"name": "Fog", "icon": "fas fa-smog text-gray"},
    "7": {"name": "Cloudy", "icon": "fas fa-cloud text-gray"},
    "8": {"name": "Overcast", "icon": "fas fa-cloud text-gray"},
    "9": {
        "name": "Light rain shower (night)",
        "icon": "fas fa-cloud-showers-heavy text-blue",
    },
    "10": {
        "name": "Light rain shower (day)",
        "icon": "fas fa-cloud-sun-rain text-yellow",
    },
    "11": {"name": "Drizzle", "icon": "fas fa-cloud-rain text-gray"},
    "12": {"name": "Light rain", "icon": "fas fa-cloud-rain text-gray"},
    "13": {
        "name": "Heavy rain shower (night)",
        "icon": "fas fa-cloud-showers-heavy text-blue",
    },
    "14": {
        "name": "Heavy rain shower (day)",
        "icon": "fas fa-cloud-sun-rain text-yellow",
    },
    "15": {"name": "Heavy rain", "icon": "fas fa-cloud-showers-heavy text-gray"},
    "16": {"name": "Sleet shower (night)", "icon": "fas fa-cloud-moon-rain text-blue"},
    "17": {"name": "Sleet shower (day)", "icon": "fas fa-cloud-sun-rain text-yellow"},
    "18": {"name": "Sleet", "icon": "fas fa-snowflake text-white"},
    "19": {"name": "Hail shower (night)", "icon": "fas fa-cloud-moon-rain text-blue"},
    "20": {"name": "Hail shower (day)", "icon": "fas fa-cloud-sun-rain text-yellow"},
    "21": {"name": "Hail", "icon": "fas fa-snowflake text-gray"},
    "22": {"name": "Light snow shower (night)", "icon": "fas fa-snowflake text-blue"},
    "23": {"name": "Light snow shower (day)", "icon": "fas fa-snowflake text-yellow"},
    "24": {"name": "Light snow", "icon": "fas fa-snowflake text-white"},
    "25": {"name": "Heavy snow shower (night)", "icon": "fas fa-snowflake text-blue"},
    "26": {"name": "Heavy snow shower (day)", "icon": "fas fa-snowflake text-yellow"},
    "27": {"name": "Heavy snow", "icon": "fas fa-snowflake text-white"},
    "28": {"name": "Thunder shower (night)", "icon": "fas fa-bolt text-blue"},
    "29": {"name": "Thunder shower (day)", "icon": "fas fa-bolt text-yellow"},
    "30": {"name": "Thunder", "icon": "fas fa-bolt text-gray"},
}

location_list = weather_api.get_location_list()


@app.route("/")
def home():
    # Logic to fetch weather data and pass it to the template
    # Render the home template and pass the weather data to it
    weather_data = weather_api.fetch_next24hrs_weather_forecast()
    # print(weather_data)
    return render_template(
        "home.html",
        weather_data=weather_data,
        weather_icon_map=weather_icon_map,
        location="Cambridge",
    )


@app.route("/filter", methods=["GET", "POST"])
def filter():
    # Logic to handle form submission and filtering of weather data
    # Render the filter template with the filtered weather data
    filtered_data = 0
    return render_template("filter.html", filtered_data=filtered_data)


@app.route("/event-planning", methods=["GET", "POST"])
def event_planning():
    # Logic to handle event planning and note-taking
    # Render the event planning template with the event data
    event_data = 0
    return render_template("event_planning.html", event_data=event_data)


@app.route("/setting", methods=["GET", "POST"])
def setting():
    # Logic to handle GPS opening/closing
    # Render the settle template
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return render_template('setting.html', name=name, email=email)
    return render_template("setting.html")

@app.route("/weather_change", methods=["POST"])
def weather_change():
    notification_api.send_email()
    return redirect("/setting")


@app.route("/forecast/<int:location_id>/<int:days_in_future>")
def forecast(location_id, days_in_future):
    weather_data = weather_api.get_future_day_location_forecast(
        location_id, days_in_future
    )
    location = ""
    for i in location_list:
        if i["id"] == str(location_id):
            location = i["name"]
            latitude = i["latitude"]
            longitude = i["longitude"]

    return render_template(
        "forecast.html",
        weather_data=weather_data,
        weather_icon_map=weather_icon_map,
        location=location,
        latitude = latitude,
        longitude = longitude
    )



@app.route('/check-requirements', methods=['POST'])
def check_requirements():
    # Extract the latitude, longitude, and selected weather from the request
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    selected_weather = data['selectedWeather']

    location_id = weather_api.get_nearest_site_id(latitude, longitude)
    print(location_id)  # 353464
    print(selected_weather)
    # Call your backend function to check the requirements and get the result
    result = weather_api.get_upcoming_days_suitable(location_id,-10,20,selected_weather)

    # Create the response JSON object
    response = {
        'locationId': location_id,
        'result': result
    }

    # Return the response as a JSON
    return jsonify(response)
