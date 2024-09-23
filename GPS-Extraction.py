from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
# from geopy.geocoders import Nominatim
from geopy.geocoders import Photon

def get_location_from_lat_lon(latitude, longitude):
    # Initialize the geolocator
    # geolocator = Nominatim(user_agent="geoapiExercises")
    geolocator = Photon(user_agent="measurements")
    
    # Create the location string
    coordinates = f"{latitude}, {longitude}"
    
    # Get the location details
    location = geolocator.reverse(coordinates, exactly_one=True)
    
    # Check if a location was found
    if location:
        return location.address
    else:
        return "Location not found"


def get_exif(image):
    exif_data = image._getexif()
    if not exif_data:
        return None
    exif = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            gps_data = {}
            for t in value:
                gps_tag = GPSTAGS.get(t, t)
                gps_data[gps_tag] = value[t]
            exif[decoded] = gps_data
        else:
            exif[decoded] = value
    return exif

def get_lat_lon(gps_info):
    if not gps_info:
        return None, None
    gps_latitude = gps_info.get('GPSLatitude')
    gps_latitude_ref = gps_info.get('GPSLatitudeRef')
    gps_longitude = gps_info.get('GPSLongitude')
    gps_longitude_ref = gps_info.get('GPSLongitudeRef')

    lat = convert_to_degrees(gps_latitude)
    if gps_latitude_ref != 'N':
        lat = -lat

    lon = convert_to_degrees(gps_longitude)
    if gps_longitude_ref != 'E':
        lon = -lon

    return lat, lon

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

## def lambda_handler(event, context):
image_path = 'images/tweet.jpg'
img = Image.open(image_path)
exif_data = get_exif(img)
if 'GPSInfo' in exif_data:
    lat, lon = get_lat_lon(exif_data['GPSInfo'])
    location = get_location_from_lat_lon(lat, lon)
    print(location)
    # print('Latitude:',lat,'Longitude:',lon)
else:
    print('error: No GPS data found')

