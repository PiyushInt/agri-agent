import json

def get_soil_data(location_id: str) -> str:
    """Retrieves simulated soil data for a given region."""
    # In a real app, this would hit an IoT / sensor API 
    data = {
        "region_1": {"ph": 6.2, "nitrogen_mg_kg": 45, "moisture_percent": 30, "soil_type": "Clay Loam"},
        "region_2": {"ph": 7.8, "nitrogen_mg_kg": 20, "moisture_percent": 15, "soil_type": "Sandy"}
    }
    return json.dumps(data.get(location_id, {"ph": 7.0, "nitrogen_mg_kg": 30, "moisture_percent": 25, "soil_type": "Loam"}))

def get_weather_forecast(location_id: str) -> str:
    """Retrieves a simulated weather forecast for the location."""
    forecasts = {
        "region_1": {"forecast": "Heavy rainfall expected tomorrow", "temp_c": 22},
        "region_2": {"forecast": "Dry and sunny", "temp_c": 35}
    }
    return json.dumps(forecasts.get(location_id, {"forecast": "Clear skies", "temp_c": 25}))

def get_market_prices(crop: str) -> str:
    """Retrieves simulated local market prices for crops."""
    prices = {
        "wheat": "2500 INR/Quintal",
        "rice": "3000 INR/Quintal",
        "cotton": "6000 INR/Quintal"
    }
    return prices.get(crop.lower(), "Price data unavailable")

def list_approved_chemicals(crop: str) -> str:
    """Lists chemicals and pesticides approved by the local agricultural board."""
    approved = {
        "wheat": ["Urea", "DAP", "Mancozeb"],
        "cotton": ["Imidacloprid", "Spinosad"]
    }
    return json.dumps(approved.get(crop.lower(), []))
