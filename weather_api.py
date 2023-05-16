import datetime
import requests

api_key = "070fea15-32d3-4422-80a7-1a0e3353d18a"

def fetch_hourly_weather_data(location_id = "350731"):
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
                    "temperature": rep['T'],
                    "humidity": rep['H'],
                    "weatherType": rep['W'],  # Assuming this is the weather type
                }
                # Add condition to filter out data older than 24 hours
                if datetime.datetime.strptime(hour_data['date'] + "T" + hour_data['hour'], "%Y-%m-%dT%H:%M") >= datetime.datetime.now() and datetime.datetime.strptime(hour_data['date'] + "T" + hour_data['hour'], "%Y-%m-%dT%H:%M") < datetime.datetime.now() + datetime.timedelta(days=1):
                    hourly_data.append(hour_data)

        return hourly_data

    else:
        # Log an error message if the request was not successful
        print(f"Error: Received status code {response.status_code} from the API")
        return []


def get_location_list():
    url = f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/sitelist?key={api_key}"
    response = requests.get(url)
    xml_data = response.content
    location_list = []
    for location in xml_data.findall('Location'):
        name = location.find('name').text
        id = location.find('id').text
        latitude = location.find('latitude').text
        longitude = location.find('longitude').text
        elevation = location.find('elevation').text
        country = location.find('country').text
        continent = location.find('continent').text
        location_list.append({'name': name, 'id': id, 'latitude': latitude, 'longitude': longitude, 'elevation': elevation, 'country': country, 'continent': continent})
    return location_list