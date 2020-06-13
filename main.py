import sys
sys.path.append('classes')

import json
from baum import DBaum

# read a file
with open('resources/data/kataster.json', 'r') as katasterfile:
#with open('resources/gsz.baumkataster_baumstandorte.json', 'r') as katasterfile:
    data = katasterfile.read()

# parse the file
obj = json.loads(data);
baeume = obj['features']
baumlist = []
for baum in baeume:
    coord = baum['geometry']['coordinates']
    b = DBaum(coord[1],coord[0])
    baumlist.append(b)

print('Read ' + str(len(baumlist)) + ' Baeume')

#dbscan
def add_neighbors(refbaum, baumlist, eps):
    for baum in baumlist:
       if refbaum == baum:
           continue
       if refbaum.getDistanceTo(baum) <= eps:
           refbaum.add_neighbor(baum)

def dbscan(dbaum_list, eps, min_pts):
    clusters = -1 # count the number of clusters and is used for cluster id assignment 
    for dbaum in dbaum_list:
        if dbaum.clusterId >= 0:
            continue
        add_neighbors(dbaum, dbaum_list, eps)
        if len(dbaum.neighbors) < min_pts:
            dbaum.setClusterId(-2)
            continue
        clusters = clusters + 1
        dbaum.setClusterId(clusters)
        seed = dbaum.neighbors.copy() # cluster seed; contains potential baum for this cluster.
        for potential_baum in seed:
            if potential_baum.clusterId == -2:
                potential_baum.setClusterId(clusters)
            if potential_baum.clusterId >= 0: 
                continue
            potential_baum.setClusterId(clusters)
            add_neighbors(potential_baum, dbaum_list, eps)
            if len(potential_baum.neighbors) >= min_pts:
                seed.extend(potential_baum.neighbors)
    return clusters + 1
print('There are ' + str(dbscan(baumlist, 20,5)) + ' clusters')

#for dbaum in baumlist
rawJson = []
for dbaum in baumlist:
    rawJson.append(dbaum.getDictForGeoJson())

# save as json file again
json_file = open("result.json", "w")
json_file.write(json.dumps(rawJson,indent=4))
json_file.close()
