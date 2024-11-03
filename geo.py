from shapely.geometry import Polygon, Point 
from database_connect import get_places, add_place
 

def check_location(location):
    polygons = []
    places = get_places()
    for place in places:
        polygons.append(Polygon(place[1]))

    point = Point(location.latitude, location.longitude)

    polygons_true = []
    for p in polygons:
        if p.contains(point):
            polygons_true.append(True)
        else: 
            polygons_true.append(False)
    if any(polygons_true):
        return True
    else:
        return False
    