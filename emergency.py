import requests

def find_nearby_hospitals(api_key, latitude, longitude, radius=3000):
    """
    Fetches nearby hospitals within the given radius from specified latitude and longitude.
    
    Parameters:
        api_key (str): Your Google Places API key.
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        radius (int): Search radius in meters (default 3000 m).
        
    Returns:
        List of dicts containing hospital name, address, and phone number.
    """
    # Nearby search endpoint
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Parameters for nearby search
    params = {
        "location": f"{latitude},{longitude}",
        "radius": radius,
        "type": "hospital",
        "key": api_key
    }
    
    # Make request to find nearby hospitals
    response = requests.get(nearby_url, params=params)
    results = response.json().get("results", [])
    
    hospitals = []
    
    # Place details endpoint to get phone
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    for place in results:
        hospital = {}
        hospital['name'] = place.get('name')
        hospital['address'] = place.get('vicinity')  # Basic address
        
        # Get place_id to fetch detailed info for phone number
        place_id = place.get('place_id')
        
        if place_id:
            details_params = {
                "place_id": place_id,
                "fields": "formatted_phone_number",
                "key": api_key
            }
            details_resp = requests.get(details_url, params=details_params)
            details_result = details_resp.json().get('result', {})
            phone = details_result.get('formatted_phone_number')
            hospital['phone'] = phone if phone else "Phone not available"
        else:
            hospital['phone'] = "Phone not available"
        
        hospitals.append(hospital)
    
    return hospitals

# Example usage:
if __name__ == "__main__":
    API_KEY = "YOUR_GOOGLE_PLACES_API_KEY"
    lat, lon = 28.6139, 77.2090  # Example coordinates (New Delhi)
    
    nearby_hospitals = find_nearby_hospitals(API_KEY, lat, lon)
    
    for h in nearby_hospitals:
        print(f"Name: {h['name']}")
        print(f"Address: {h['address']}")
        print(f"Phone: {h['phone']}")
        print("-" * 40)
