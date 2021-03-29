import googlemaps
from config.config import ConfigReader

class GoogleMapsService():
    def __init__(self):
        self.config_reader = ConfigReader()
        self.configuration = self.config_reader.read_config()
        self.maps_api_key = self.configuration['GOOGLE_PLACES_API_KEY']
        self.gmaps = googlemaps.Client(key = self.maps_api_key)
        self.index = 0
    
    def find_nearest(self, food_type: str, location: str):
        maploc = self.gmaps.geocode(address = location)
        location = maploc[0]['geometry']['location']
        loc_str = str(location['lat']) + "," + str(location['lng'])
        place_result = self.gmaps.places_nearby(location=loc_str, keyword=food_type, radius=10000, type = 'restaurant')
        self.results = place_result['results']
        return self.results[0]
    
    def find_next():
        self.index += self.index
        return self.results[index] if len(self.results) > self.index else None