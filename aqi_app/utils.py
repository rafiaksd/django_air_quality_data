import requests

def pm25_to_aqi(pm25):
    # Simplified AQI calculation (replace with your actual logic)
    if pm25 < 0:
        return 0
    elif pm25 <= 12:
        return int((50 / 12) * pm25)
    elif pm25 <= 35.4:
        return int(((100 - 51) / (35.4 - 12.1)) * (pm25 - 12.1) + 51)
    else:
        return 100  # Extend as needed

def aqi_to_cigars_per_day(aqi):
    # Simplified conversion (replace with your actual logic)
    return aqi / 50  # Example: 1 cigarette per 50 AQI points

def aqi_to_health_label(aqi):
    if aqi <= 50:
        return "good"
    elif aqi <= 100:
        return "moderate"
    else:
        return "unhealthy"

def get_sensor_type_from_url(url):
    if "purpleair" in url.lower():
        return "PurpleAir"
    return "Unknown"

def extract_pm25_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Replace with actual JSON parsing based on your sensor API
        return float(data.get('pm25', -1))
    except:
        return -1
