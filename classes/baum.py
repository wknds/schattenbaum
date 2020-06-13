from utils import haversine_distance
class DBaum: 

    longitude = 0
    latitude = 0
    clusterId = -1 # -1 means unvisited, -2 means noise. >=0 are cluster ids
    neighbors = []

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def setClusterId(self, clusterId):
        self.clusterId = clusterId

    def getDistanceTo(self, baum):
        # the returned distance between this and the given baum (in metre)
        return 1000*haversine_distance(self.latitude, self.longitude, baum.latitude, baum.longitude) 

    def add_neighbor(self, baum):
        if self is not baum:
            self.neighbors.append(baum)

    def getDictForGeoJson(self):
        return {
                "type": "Feature",
                "geometry": "Point",
                "coordinates": [self.longitude, self.latitude],
                "properties": {
                    "clusterid": self.clusterId
                    }
                }
