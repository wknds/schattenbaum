import json
import numpy as np
from classes.baum import Baum 

# read a file
with open('resources/data/kataster.json', 'r') as katasterfile:
    data = katasterfile.read()

# parse the file
obj = json.loads(data);
#print(json.dumps(obj['features'], indent=4))
baeume = obj['features']
baumlist = []
for baum in baeume:
    coord = baum['geometry']['coordinates']
    b = Baum(coord[1],coord[0])
    baumlist.append(b)

# test this formula
def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res, 2)

lon1 = baeume[6]['geometry']['coordinates'][0]
lat1 = baeume[6]['geometry']['coordinates'][1]
lon2 = baeume[1]['geometry']['coordinates'][0]
lat2 = baeume[1]['geometry']['coordinates'][1]
print(str(haversine_distance(47.41093,8.56686,47.41102,8.56740)) + " km")

print(str(haversine_distance(lat1, lon1, lat2, lon2)) + " km")

