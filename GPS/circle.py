import math
import slumber 
import re
    
def get_geolocation(self, *args, **kwargs):
    """
    >>> get_geolocation("Trinity College Dublin", "Dublin", country="Ireland")
    {'latitude': '53.42521010000001', 'longitude': '-6.05255'}
    """
    arglist = []
    for key, value in enumerate(args):
        arglist.append(value)
    user_location = ", ".join(arglist)
    maps_api = slumber.API("http://maps.googleapis.com/maps/api/", append_slash=False)
    
    if 'country' in kwargs:
        google_reply = str( maps_api.geocode.json.get(address=user_location, components="country:"+kwargs['country'], sensor="false") )
    else:
        google_reply = str( maps_api.geocode.json.get(address=user_location, sensor="false") )
    
    match = re.search(r'(?<=lat\':\s)[\d\.\-]*', google_reply)
    if match:                      
        latitude = match.group()
    else:
        return None
    
    match = re.search(r'(?<=lng\':\s)[\d\.\-]*', google_reply)
    if match:                      
        longitude = match.group()
        
    return {'latitude': latitude, 'longitude':longitude}