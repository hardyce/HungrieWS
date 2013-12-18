import math
import slumber 
import re

def within_radius(self, origin, destination, **kwargs):
    lat1 = origin.get('latitude')
    lon1 = origin.get('longitude')
    
    lat2 = destination.get('latitude')
    lon2 = destination.get('longitude')

    
    earthRadius = 6371; # Radius of earth in km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = earthRadius * c
    
    if 'radius' in kwargs:
        my_radius = kwargs['country']
        if distance == my_radius:
            return True
        else:
            return False
    else:  
        return distance
    
def get_geolocation(self, *args, **kwargs):
    arglist = []
    for key, value in enumerate(args):
        arglist.append(value)
    user_location = ", ".join(arglist)
    maps_api = slumber.API("http://maps.googleapis.com/maps/api/", append_slash=False)
    
    print user_location
    
    if 'country' in kwargs:
        print kwargs['country']
        google_reply = str( maps_api.geocode.json.get(address=user_location, components="country:"+kwargs['country'], sensor="false") )
    else:
        google_reply = str( maps_api.geocode.json.get(address=user_location, sensor="false") )
    
    print google_reply
    
    match = re.search(r'(?<=lat\':\s)[\d\.\-]*', google_reply)
    if match:                      
        latitude = match.group()
    else:
        return None
    
    match = re.search(r'(?<=lng\':\s)[\d\.\-]*', google_reply)
    if match:                      
        longitude = match.group()
        
    print longitude
    return {'latitude': latitude, 'longitude':longitude}