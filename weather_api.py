import datetime
import requests

api_key = "070fea15-32d3-4422-80a7-1a0e3353d18a"

def fetch_next24hrs_weather_forecast(location_id = "350731"):
    base_url = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/"
    url = f"{base_url}{location_id}?res=3hourly&key={api_key}"

    response = requests.get(url)

    # Check that the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract the weather data from the response
        weather_reports = data['SiteRep']['DV']['Location']['Period']

        # Prepare the list to hold the hourly data
        hourly_data = []

        # Iterate over the weather reports to extract hourly data
        for report in weather_reports:
            date = report['value'][:-1]  # Extract date from 'value' field
            
            for rep in report['Rep']:
                # Convert minutes past midnight to hour
                hour = int(rep['$']) // 60

                hour_data = {
                    "date": date,
                    "hour": f"{hour:02d}:00",  # Formatting the hour
                    "temperature": float(rep['T']),
                    "humidity": rep['H'],
                    "weatherType": rep['W'],  # Assuming this is the weather type
                }
                # Add condition to filter out data older than 24 hours
                if datetime.datetime.strptime(hour_data['date'] + "T" + hour_data['hour'], "%Y-%m-%dT%H:%M") >= datetime.datetime.now() and datetime.datetime.strptime(hour_data['date'] + "T" + hour_data['hour'], "%Y-%m-%dT%H:%M") < datetime.datetime.now() + datetime.timedelta(days=1):
                    hour_data['date']=str(hour_data['date'])[5:]
                    hourly_data.append(hour_data)

        return hourly_data

    else:
        # Log an error message if the request was not successful
        print(f"Error: Received status code {response.status_code} from the API")
        return []



def get_location_list():
    url = f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key={api_key}"
    response = requests.get(url)
    json_data = response.json()
    location_list = []
    for location in json_data['Locations']['Location']:
        name = location['name']
        id = location['id']
        latitude = location['latitude']
        longitude = location['longitude']
        location_list.append({'name': name, 'id': id, 'latitude': latitude, 'longitude': longitude})
    return location_list

def get_nearest_site_id(latitude, longitude):
    # This function returns the ID of the neareset weather site from the given coordinates
    # Example: get_nearest_site_id(52.21097235154088, 0.09139787817833253)
    # This returns 310042, as this is the ID of Cambridge site, which is nearest.
    nearest_distance = 1E69
    nearest_id = -1
    sites = requests.get(f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key={api_key}").json()['Locations']['Location']
    for site in sites:
        distance = ((latitude - float(site['latitude'])) ** 2 + (longitude - float(site['longitude'])) ** 2) ** 0.5
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_id = site['id']
    return nearest_id

def get_future_day_location_forecast(location_id, target_date):
    base_url = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/"
    url = f"{base_url}{location_id}?res=3hourly&key={api_key}"

    response = requests.get(url)

    # Check that the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract the weather data from the response
        weather_reports = data['SiteRep']['DV']['Location']['Period']

        # Prepare the list to hold the hourly data
        hourly_data = []

        # Calculate the target date
        today = datetime.datetime.now().date()
        target_date = today + datetime.timedelta(days=target_date)

        # Iterate over the weather reports to extract hourly data
        for report in weather_reports:
            date = report['value'][:-1]  # Extract date from 'value' field

            # Convert the date to a datetime object
            report_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

            # Check if the report date matches the target date
            if report_date == target_date:
                for rep in report['Rep']:
                    # Convert minutes past midnight to hour
                    hour = int(rep['$']) // 60

                    hour_data = {
                        "date": str(date)[5:],
                        "hour": f"{hour:02d}:00",  # Formatting the hour
                        "temperature": float(rep['T']),
                        "humidity": rep['H'],
                        "weatherType": rep['W'],  # Assuming this is the weather type
                    }
                    hourly_data.append(hour_data)

        return hourly_data

    else:
        # Log an error message if the request was not successful
        print(f"Error: Received status code {response.status_code} from the API")
        return []





if __name__ == "__main__":
    print(len(get_location_list()))
    # print(get_future_day_location_forecast(310069,1))

def get_upcoming_suitable_datetimes(location_id, min_temp, max_temp, weather_types):
    """ Returns a list of upcoming dates/times tuples that fit the given requirements """
    # min_temp, max_temp, are all numbers, weather_types is a list of weather_type:
    # weather type strings: ["sunny", "cloudy", "rainy", "snowy", "windy"]
    # Note that "windy" is not a weather code in the API but this function treats a wind speed of over 23mph to be "windy"
    url = f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{location_id}?res=3hourly&key={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} from the API")
        return []
    data = response.json()
    weather_reports = data['SiteRep']['DV']['Location']['Period']

    suitable_datetimes = []
    for day in weather_reports:
        date = day['value']
        for rep in day['Rep']:
            minutes = int(rep['$']) # Minutes after UTC
            pp = float(rep['Pp']) # Precipitation probability in percentage
            s = float(rep['S']) # Wind speed (mph)
            t = float(rep['T']) # Temp in C
            w = int(rep['W']) # Weather code, 0 = clear night, 1 = sunny day, (...) 30 = thunder
            if not min_temp <= t <= max_temp:
                continue
            if w in [0, 1]: weather_type = "sunny"
            if w in [2, 3, 5, 6, 7, 8]: weather_type = "cloudy"
            if w in [9, 10, 11, 12, 13, 14, 15, 28, 29, 30]: weather_type = "rainy"
            if w in [22, 23, 24, 25, 26, 27, 28]: weather_type = "snowy"
            if weather_type not in weather_types:
                if "windy" not in weather_types:
                    continue
                if "windy" in weather_types and s < 23:
                    continue

            # Don't need to check weather_type == "ANYTHING" because anything goes
            suitable_datetimes.append((date, minutes))
    return suitable_datetimes

def get_upcoming_days_suitable(location_id, min_temp, max_temp, weather_types):
    """ Returns a list of 5 booleans representing whether or not the next 5 days contain a time that fits the given requirements """
    # Example usage:
    # get_upcoming_days_suitable(350731, 0, 10, ["sunny", "cloudy"])
    # Returns [False, True, True, True, True]
    # Representing that tomorrow and the day after tomorrow fit the requirements: location 350731, temperature between 0 to 10, weather type sunny or cloudy

    suitable_datetimes = get_upcoming_suitable_datetimes(location_id, min_temp, max_temp, weather_types)
    suitable_days = []
    today = datetime.date.today()
    for i in range(5):
        print(1, suitable_datetimes)
        print(2, [(datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y-%m-%dZ") == dt[0] for dt in suitable_datetimes])
        suitable_days.append(any([(datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y-%m-%dZ") == dt[0] for dt in suitable_datetimes]))
    return suitable_days

print(get_upcoming_days_suitable(350731, 0, 10, ["sunny", "cloudy"]))