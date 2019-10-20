from geopy.geocoders import Nominatim

def convert_to_long_lat(loc):
    """Given a string address. Parses and returns the longtitude and latitude."""
   
    geolocator = Nominatim(user_agent="easyshot_user_locator")
    location = geolocator.geocode(loc)
    # i.e. "175 5th Avenue NYC"
    # print(location.address)
    # Flatiron Building, 175, 5th Avenue, Flatiron District, Manhattan Community Board 5, Manhattan, New York County, NYC, New York, 10010, USA
    return (location.latitude, location.longitude)
