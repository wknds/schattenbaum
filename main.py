import sys
sys.path.append('/home/yaw/git/baumschatten/classes')

import json
from baum import DBaum

# read a file
#with open('resources/data/kataster.json', 'r') as katasterfile:
with open('resources/gsz.baumkataster_baumstandorte.json', 'r') as katasterfile:
    data = katasterfile.read()

# parse the file
obj = json.loads(data);
baeume = obj['features']
baumlist = []
for baum in baeume:
    coord = baum['geometry']['coordinates']
    cat = baum['properties']['kategorie']
    quartier = baum['properties']['quartier']

    if cat == "Parkbaum" and quartier == "Oerlikon":
        b = DBaum(coord[1],coord[0])
        baumlist.append(b)

print('Read ' + str(len(baumlist)) + ' Baeume')

#dbscan
def identify_neighbors(refbaum, baumlist, eps):
    if len(refbaum.neighbors) > 0:
        return refbaum.neighbors
    for baum in baumlist:
        if refbaum == baum:
            continue
        distance = refbaum.getDistanceTo(baum)
        if distance == 0:
            baumlist.remove(baum)
        if distance <= eps and distance > 0:
            refbaum.add_neighbor(baum)
    return refbaum.neighbors
def expand_cluster(dbaumlist, clusterId, init, seed, eps, min_pts):
    if init == True:
        dbaum = seed[0]
        if dbaum.clusterId >= 0 or dbaum.clusterId == -2:
            return seed
        neighbors = identify_neighbors(dbaum, dbaumlist, eps)
        if len(neighbors) == 0:
            dbaumlist.remove(dbaum)
            return seed
        return expand_cluster(dbaumlist, clusterId, False, seed, eps, min_pts)
    for dbaum in seed:
        if dbaum.clusterId == -2: # noise
            dbaum.setClusterId(clusterId)
        if dbaum.clusterId >= 0:
            continue
        dbaum.clusterId = clusterId
        dbaum.on_seeding = True
        neighbors = identify_neighbors(dbaum, dbaumlist, eps)
        if len(neighbors) >= min_pts:
            next_seed = []
            for neighbor in neighbors:
                if neighbor.on_seeding == False:
                    next_seed.append(neighbor)
                    neighbor.on_seeding = True
            seed.extend(expand_cluster(dbaumlist, clusterId, False, next_seed, eps, min_pts))
            #return seed
        else:
            dbaum.clusterId = -2
    return seed

def dbscan(dbaum_list, eps, min_pts):
    clusters = 0 # count the number of clusters and is used for cluster id assignment 
    progress = 0
    for dbaum in dbaum_list:
        dbaum.on_seeding = True
        progress = progress + 1
        if progress % 100 == 0:
            print("Progress: " + str(progress) + " Baeume (von " + str(len(dbaum_list))  + "). Clusters found: " + str(clusters+1))
        if dbaum.clusterId >= 0:
            dbaum.on_seeding = False
            continue
        seed = [dbaum]
        seed = expand_cluster(dbaum_list, clusters, True, seed, eps, min_pts)
        if len(seed) > 1:
            clusters = clusters + 1
        for potential_baum in seed:
            potential_baum.on_seeding = False
        dbaum.on_seeding = False
    return clusters + 1

copybaumlist = baumlist.copy()
eps = 15
min_pts = 10
print('There are ' + str(dbscan(baumlist, eps, min_pts)) + ' clusters')

#for dbaum in baumlist
rawJson = []
for dbaum in copybaumlist:
    if dbaum.clusterId >= 0:
        rawJson.append(dbaum.getDictForGeoJson())
rawJson = {
        "type": "FeatureCollection",
        "features": rawJson
        }

# save as json file again
path = "result_eps_"+ str(eps) + "_pts_" + str(min_pts) + ".json"
json_file = open(path, "w")
json_file.write(json.dumps(rawJson,indent=4))
json_file.close()
