from models import Location
from distance_matrix import get_distance_matrix

locs = [
    Location(id="delhi", name="Delhi", lat=28.7041, lon=77.1025),
    Location(id="agra", name="Agra", lat=27.1767, lon=78.0081)
]
d, t = get_distance_matrix(locs)
print("Distance Matrix:", d)