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

def extract_pm25_from_url(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise error if bad response

        data = response.json()

        # Check if it's AirGradient
        if "airgradient.com" in api_url:
            print(f"AirGradient sensor detected... fetching pm2.5 data...")
            return float(data.get("pm02", -1))

        # Check if it's PurpleAir
        elif "purpleair.com" in api_url:
            print(f"PurpleAir sensor detected... fetching pm2.5 data...")
            return float(data.get("sensor", {}).get("pm2.5", -1))
        
        # IQAir format
        elif "airvisual.com" in api_url or "iqair" in api_url:
            print("IQAir sensor detected... fetching pm2.5 data...")
            try:
                aqius = extract_aqius_from_data(data)
                if aqius is None:
                    return -1
                
                pm25 = aqius_to_pm25(aqius)
                return float(pm25)
                #return float(data["data"]["current"]["pollution"]["aqius"])
            except (KeyError, TypeError) as e:
                print(f"[IQAir] JSON structure unexpected: {e}")
                return -1
        else:
            print("Unknown API format.")
            return -1

    except Exception as e:
        print(f"Error: {e}")
        return -1

def aqius_to_pm25(aqius):
    breakpoints = [
        (0, 50, 0.0, 12.0),
        (51, 100, 12.1, 35.4),
        (101, 150, 35.5, 55.4),
        (151, 200, 55.5, 150.4),
        (201, 300, 150.5, 250.4),
        (301, 400, 250.5, 350.4),
        (401, 500, 350.5, 500.4),
    ]

    for I_low, I_high, C_low, C_high in breakpoints:
        if I_low <= aqius <= I_high:
            pm25 = ((aqius - I_low) * (C_high - C_low) / (I_high - I_low)) + C_low
            return round(pm25, 2)
    return None
 
# for IQ Air API Data
def extract_aqius_from_data(data):
    try:
        return data.get('data', {}).get('current', {}).get('pollution', {}).get('aqius')
    except AttributeError:
        return None