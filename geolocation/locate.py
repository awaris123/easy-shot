from geopy.geocoders import Nominatim

PRIMARY_CARE_DB = '../data/primary_care_loc.csv'
FLU_DB = '../data/flushot_locs_19-20.csv'


def convert_to_long_lat(loc):
    """Given a string address. Parses and returns the longtitude and latitude."""
   
    geolocator = Nominatim(user_agent="easyshot_user_locator")
    location = geolocator.geocode(loc)
    # i.e. > "175 5th Avenue NYC"
    # print(location.address)
    # > Flatiron Building, 175, 5th Avenue, Flatiron District, Manhattan Community Board 5, Manhattan, New York County, NYC, New York, 10010, USA
    return (location.latitude, location.longitude)






pk_df = pd.read_csv(PRIMARY_CARE_DB)
    
def primary_facility_phone(address):
    """Takes a string address as the user location and returns the closest primary care center location."""

    _latlong = convert_to_long_lat(address)  #<-- This is from the locate.py
    selectedindex = pk_df[["latitude", "longtitude"]].sub(_latlong).pow(2).sum(1).pow(0.5).idxmin() 
    
    SELECTED = pk_df.iloc[selectedindex]
    SELECTED_FACILITY = SELECTED[1]
    SELECTED_PHONE = SELECTED[3]
    SELECTED_COORDINATE = SELECTED[12],SELECTED[13]
    
    return (SELECTED_COORDINATE[0], SELECTED_COORDINATE[1], SELECTED_FACILITY, SELECTED_PHONE)



flu_df = pd.read_csv("../data/flushot_locs_19-20.csv")

def flu_facility_phone(address):
    """Takes a string address as the user location and returns the closest flu shot location."""
    
    
    _latlong = convert_to_long_lat(address)  #<-- This is from the locate.py
    selectedindex = flu_df[["Latitude", "Longitude"]].sub(_latlong).pow(2).sum(1).pow(0.5).idxmin() 

    SELECTED = flu_df.iloc[selectedindex]
    # print(SELECTED)
    SELECTED_FACILITY = SELECTED[11]
    SELECTED_PHONE = SELECTED[13]
    SELECTED_COORDINATE = SELECTED[3],SELECTED[4]

    return (SELECTED_COORDINATE[0], SELECTED_COORDINATE[1], SELECTED_FACILITY, SELECTED_PHONE)