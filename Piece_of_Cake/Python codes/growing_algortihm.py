import pandas as pd
import numpy as np

numberofVoxels = len(xcoordinates)
counter = 10  #10 starting points of the functions are already given

#defining the caracteristics of each function
maxSurfaceAtrium = p*500 / 16
maxShadowValueAtrium = 1
minNoiseValueAtrium = 0
#264
maxSurfaceStudenthousing = p*2000 / 16
maxShadowValueStudenthousing = 1
minNoiseValueStudenthousing = 0.07

maxSurfaceAssistedhousing = p*1180 / 16
maxShadowValueAssistedhousing = 1
minNoiseValueAssistedhousing = 0.75
#1180
maxSurfaceStarterhousing = p*3180 / 16
maxShadowValueStarterhousing = 1
minNoiseValueStarterhousing = 0.372

maxSurfaceWorkspace = p*600 / 16
maxShadowValueWorkspace = 1
minNoiseValueWorkspace = 0.3
#540
maxSurfaceRestaurant = p*152 / 16
maxShadowValueRestaurant = 1
minNoiseValueRestaurant = 0
#120
maxSurfaceCinema = p*90 / 16
maxShadowValueCinema = 1
minNoiseValueCinema = 0

maxSurfaceGym = p*144 / 16
maxShadowValueGym = 1
minNoiseValueGym = 0
#80
maxSurfaceSupermarket = p*300 / 16
maxShadowValueSupermarket = 1
minNoiseValueSupermarket = 0

#0=function has not yet reached the maximum surface; 
#1=function has reached the maximum surface OR there aren't any available voxels anymore
atriumFull = 0
studenthousingFull = 0
assistedhousingFull = 0
starterhousingFull = 0
workspaceFull = 0
restaurantFull = 0
cinemaFull = 0
gymFull = 0
supermarketFull = 0

#creating the dataframe with colums for the coordinates, shadowvalues, noisevalues and function of each point in the pointcloud
df = pd.DataFrame({'x': xcoordinates, 'y': ycoordinates, 'z': zcoordinates, 'shadowvalues': shadowvalues, 'noisevalues': noisevalues, 'functions': -1})
#setting the label in the 'function' column to the corresponding number for all the starting points
df.loc[firstAtriumIndex, 'functions'] = 0 #Atrium = 0
#all voxels above the starting point of the atrium should also be included because the atrium will reach to the top of the building
for j in df.index[df.functions == 0].values:
    acceptedcandidates_z = df[(df.x == df.loc[j, 'x']) & (df.y == df.loc[j, 'y'])]
    df.loc[acceptedcandidates_z.index.values, 'functions'] = 0 
df.loc[firstStudenthousingIndex, 'functions'] = 1 #studenthousing = 1
df.loc[firstAssistedhousingIndex, 'functions'] = 2 #assistedhousing = 2
df.loc[firstStarterhousingIndex, 'functions'] = 3 #starterhousing = 3
df.loc[firstWorkspaceIndex, 'functions'] = 4 #workspace = 4
#for evey point set to a public function, the point direct above it should also be included as all the public functions will have a double height ceiling
for j in df.index[df.functions == 4].values:
    acceptedcandidates_z = df[(df.x == df.loc[j, 'x']) & (df.y == df.loc[j, 'y']) & (df.z == (df.loc[j, 'z']+1))]
    df.loc[acceptedcandidates_z.index.values, 'functions'] = 4 
df.loc[firstRestaurantIndex, 'functions'] = 5 #restaurant = 5
for j in df.index[df.functions == 5].values:
    acceptedcandidates_z = df[(df.x == df.loc[j, 'x']) & (df.y == df.loc[j, 'y']) & (df.z == (df.loc[j, 'z']+1))]
    df.loc[acceptedcandidates_z.index.values, 'functions'] = 5
df.loc[firstCinemaIndex, 'functions'] = 6 #cinema = 6
for j in df.index[df.functions == 6].values:
    acceptedcandidates_z = df[(df.x == df.loc[j, 'x']) & (df.y == df.loc[j, 'y']) & (df.z == (df.loc[j, 'z']+1))]
    df.loc[acceptedcandidates_z.index.values, 'functions'] = 6
df.loc[firstGymIndex, 'functions'] = 7 #gym = 7
for j in df.index[df.functions == 7].values:
    acceptedcandidates_z = df[(df.x == df.loc[j, 'x']) & (df.y == df.loc[j, 'y']) & (df.z == (df.loc[j, 'z']+1))]
    df.loc[acceptedcandidates_z.index.values, 'functions'] = 7
df.loc[firstSupermarketIndex, 'functions'] = 8 #supermarket = 8
for j in df.index[df.functions == 8].values:
    acceptedcandidates_z = df[(df.x == df.loc[j, 'x']) & (df.y == df.loc[j, 'y']) & (df.z == (df.loc[j, 'z']+1))]
    df.loc[acceptedcandidates_z.index.values, 'functions'] = 8

#following while loop will loop through every growing function untill there are no more points left over in the 
#building OR untill all the maximum surfaces of the functions have been reached
while (counter < numberofVoxels) & (atriumFull*studenthousingFull*assistedhousingFull*starterhousingFull*workspaceFull*restaurantFull*cinemaFull*gymFull*supermarketFull == 0):
    #every function will loop through the current function points, find the available neighbours, 
    #check if they have the minimum required noisevalue, and from the leftover options 
    #select the points that are closest in distance to a sunlit area and to another function given the network from the graph relaxation

    if (len(df[df.functions == 0]) / 7) < maxSurfaceAtrium:
        countaccepted = 0
        atriumPoints = df[df.functions == 0]
        atriumIndices = atriumPoints.index[atriumPoints.z == 0].values
        for i in atriumIndices: 
            xneighbours = df[((df.x == (df.loc[i, 'x'] + 1)) | (df.x == (df.loc[i, 'x'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.z == (df.loc[i, 'z']))]
            yneighbours = df[((df.y == (df.loc[i, 'y'] + 1)) | (df.y == (df.loc[i, 'y'] - 1))) & (df.x == (df.loc[i, 'x'])) & (df.z == (df.loc[i, 'z']))]
            neighbours = pd.concat([xneighbours, yneighbours])
            candidates = neighbours[neighbours.functions == -1]
            acceptedCandidates = candidates[(candidates.shadowvalues <= maxShadowValueAtrium) & (candidates.noisevalues >= minNoiseValueAtrium)]
            #select the point that is closest to the other side of the building, that way, the atrium will have a better chance at connecting all the functions of the building
            mindist = 1000
            closestCandidate = firstAtriumIndex
            mindist2 = 1000
            closestCandidate2 = firstAtriumIndex
            for k in acceptedCandidates.index.values: 
                dist = np.sqrt((df.loc[k, 'x'] - df.loc[127, 'x'])**2 + (df.loc[k, 'y'] - df.loc[127, 'y'])**2) 
                if dist < mindist:
                    mindist = dist
                    closestCandidate = k
                dist2 = np.sqrt((df.loc[k, 'x'] - df.loc[213, 'x'])**2 + (df.loc[k, 'y'] - df.loc[213, 'y'])**2) 
                if dist2 < mindist2:
                    mindist2 = dist2
                    closestCandidate2 = k
            df.loc[[closestCandidate, closestCandidate2], 'functions'] = 0
            for j in [closestCandidate, closestCandidate2]:
                closestCandidate_z = df[(df.x == df.loc[j, 'x']) & (df.y == df.loc[j, 'y'])]
                df.loc[closestCandidate_z.index.values, 'functions'] = 0
            df.loc[closestCandidate_z.index.values, 'functions'] = 0
            countaccepted = countaccepted + len(acceptedCandidates)
        if countaccepted == 0: #if there are no more available neighbours found: print an error that mentions this and set the value of atriumFull to 1
            atriumFull = 1
            print('growing atrium was interrupted because no acceptable voxels found')
    if (len(df[df.functions == 0]) / 7) >= maxSurfaceAtrium: #if the maximum surface of the atrium is reached: set the value of atriumFull to 1
        atriumFull = 1

    
    if len(df[df.functions == 1]) < maxSurfaceStudenthousing:
        countaccepted = 0
        studenthousingIndices = df.index[df.functions == 1].values
        for i in studenthousingIndices: 
            xneighbours = df[((df.x == (df.loc[i, 'x'] + 1)) | (df.x == (df.loc[i, 'x'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.z == (df.loc[i, 'z']))]
            yneighbours = df[((df.y == (df.loc[i, 'y'] + 1)) | (df.y == (df.loc[i, 'y'] - 1))) & (df.x == (df.loc[i, 'x'])) & (df.z == (df.loc[i, 'z']))]
            zneighbours = df[((df.z == (df.loc[i, 'z'] + 1)) | (df.z == (df.loc[i, 'z'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.x == (df.loc[i, 'x']))]
            neighbours = pd.concat([xneighbours, yneighbours, zneighbours])
            candidates = neighbours[neighbours.functions == -1]
            acceptedCandidates = candidates[(candidates.shadowvalues <= maxShadowValueStudenthousing) & (candidates.noisevalues >= minNoiseValueStudenthousing)]
            #select the point that is closest to the atrium so that all functions will grow around the atrium and give the best possible network in the building
            mindist = 1000
            closestCandidate = firstStudenthousingIndex
            for k in acceptedCandidates.index.values: 
                dist = np.sqrt((df.loc[k, 'x'] - df.loc[firstAtriumIndex, 'x'])**2 + (df.loc[k, 'y'] - df.loc[firstAtriumIndex, 'y'])**2)
                if dist < mindist:
                    mindist = dist
                    closestCandidate = k
            df.loc[closestCandidate, 'functions'] = 1
            countaccepted = countaccepted + len(acceptedCandidates)
        if countaccepted == 0:
            studenthousingFull = 1
            print('growing studenthousing was interrupted because no acceptable voxels found')
    if len(df[df.functions == 1]) >= maxSurfaceStudenthousing:
        studenthousingFull = 1


    if len(df[df.functions == 2]) < maxSurfaceAssistedhousing:
        countaccepted = 0
        assistedhousingIndices = df.index[df.functions == 2].values
        for i in assistedhousingIndices: 
            xneighbours = df[((df.x == (df.loc[i, 'x'] + 1)) | (df.x == (df.loc[i, 'x'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.z == (df.loc[i, 'z']))]
            yneighbours = df[((df.y == (df.loc[i, 'y'] + 1)) | (df.y == (df.loc[i, 'y'] - 1))) & (df.x == (df.loc[i, 'x'])) & (df.z == (df.loc[i, 'z']))]
            zneighbours = df[((df.z == (df.loc[i, 'z'] + 1)) | (df.z == (df.loc[i, 'z'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.x == (df.loc[i, 'x']))]
            neighbours = pd.concat([xneighbours, yneighbours, zneighbours])
            candidates = neighbours[neighbours.functions == -1]
            acceptedCandidates = candidates[(candidates.shadowvalues <= maxShadowValueAssistedhousing) & (candidates.noisevalues >= minNoiseValueAssistedhousing)]
            mindist = 1000
            closestCandidate = firstAssistedhousingIndex
            for k in acceptedCandidates.index.values:
                dist = np.sqrt((df.loc[k, 'x'] - df.loc[firstAtriumIndex, 'x'])**2 + (df.loc[k, 'y'] - df.loc[firstAtriumIndex, 'y'])**2)
                if dist < mindist:
                    mindist = dist
                    closestCandidate = k
            df.loc[closestCandidate, 'functions'] = 2
            countaccepted = countaccepted + len(acceptedCandidates)
        if countaccepted == 0:
            assistedhousingFull = 1
            print('growing assistedhousing was interrupted because no acceptable voxels found')
    if len(df[df.functions == 2]) >= maxSurfaceAssistedhousing:
        assistedhousingFull = 1


    if len(df[df.functions == 3]) < maxSurfaceStarterhousing:
        countaccepted = 0
        starterhousingIndices = df.index[df.functions == 3].values
        for i in starterhousingIndices: 
            xneighbours = df[((df.x == (df.loc[i, 'x'] + 1)) | (df.x == (df.loc[i, 'x'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.z == (df.loc[i, 'z']))]
            yneighbours = df[((df.y == (df.loc[i, 'y'] + 1)) | (df.y == (df.loc[i, 'y'] - 1))) & (df.x == (df.loc[i, 'x'])) & (df.z == (df.loc[i, 'z']))]
            zneighbours = df[((df.z == (df.loc[i, 'z'] + 1)) | (df.z == (df.loc[i, 'z'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.x == (df.loc[i, 'x']))]
            neighbours = pd.concat([xneighbours, yneighbours, zneighbours])
            candidates = neighbours[neighbours.functions == -1]
            acceptedCandidates = candidates[(candidates.shadowvalues <= maxShadowValueStarterhousing) & (candidates.noisevalues >= minNoiseValueStarterhousing)]
            mindist = 1000
            closestCandidate = firstStarterhousingIndex
            for k in acceptedCandidates.index.values:
                dist = np.sqrt((df.loc[k, 'x'] - df.loc[firstAtriumIndex, 'x'])**2 + (df.loc[k, 'y'] - df.loc[firstAtriumIndex, 'y'])**2)
                if dist < mindist:
                    mindist = dist
                    closestCandidate = k
            df.loc[closestCandidate, 'functions'] = 3
            countaccepted = countaccepted + len(acceptedCandidates)
        if countaccepted == 0:
            starterhousingFull = 1
            print('growing starterhousing was interrupted because no acceptable voxels found')
    if len(df[df.functions == 3]) >= maxSurfaceStarterhousing:
        starterhousingFull = 1


    if (len(df[df.functions == 4])/2) < maxSurfaceWorkspace:
        countaccepted = 0
        workspacePoints = df[df.functions == 4]
        workspaceIndices = workspacePoints.index[workspacePoints.z == 0].values
        for i in workspaceIndices: 
            xneighbours = df[((df.x == (df.loc[i, 'x'] + 1)) | (df.x == (df.loc[i, 'x'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.z == (df.loc[i, 'z']))]
            yneighbours = df[((df.y == (df.loc[i, 'y'] + 1)) | (df.y == (df.loc[i, 'y'] - 1))) & (df.x == (df.loc[i, 'x'])) & (df.z == (df.loc[i, 'z']))]
            neighbours = pd.concat([xneighbours, yneighbours])
            candidates = neighbours[neighbours.functions == -1]
            acceptedCandidates = candidates[(candidates.shadowvalues <= maxShadowValueWorkspace) & (candidates.noisevalues >= minNoiseValueWorkspace)]
            mindist_a = 1000
            closestCandidate_a = firstWorkspaceIndex
            #select the point that is closest to the edge of the building where there is more sunlight
            mindist_e = 1000
            closestCandidate_e = firstWorkspaceIndex
            mindist_e2 = 1000
            closestCandidate_e2 = firstWorkspaceIndex
            for k in acceptedCandidates.index.values:
                #dist_a = np.sqrt((df.loc[k, 'x'] - df.loc[firstAtriumIndex, 'x'])**2 + (df.loc[k, 'y'] - df.loc[firstAtriumIndex, 'y'])**2)
                #if dist_a < mindist_a:
                    #mindist_a = dist_a
                    #closestCandidate_a = k
                #dist_e = df.loc[k, 'x']
                #if dist_e < mindist_e:
                    #mindist_e = dist_e
                    #closestCandidate_e = k
                dist_e2 = 18 - df.loc[k, 'y']
                if dist_e2 < mindist_e2:
                    mindist_e2 = dist_e2
                    closestCandidate_e2 = k
            df.loc[[closestCandidate_a, closestCandidate_e, closestCandidate_e2], 'functions'] = 4
            for j in [closestCandidate_a, closestCandidate_e, closestCandidate_e2]:
                closestCandidate_z = df[(df.x == df.loc[j, 'x']) & (df.y == df.loc[j, 'y']) & (df.z == (df.loc[j, 'z']+1))]
                df.loc[closestCandidate_z.index.values, 'functions'] = 4
            countaccepted = countaccepted + len(acceptedCandidates)
        if countaccepted == 0:
            workspaceFull = 1
            print('growing workspace was interrupted because no acceptable voxels found')
    if (len(df[df.functions == 4])/2) >= maxSurfaceWorkspace:
        workspaceFull = 1


    if (len(df[df.functions == 5])/2) < maxSurfaceRestaurant:
        countaccepted = 0
        restaurantPoints = df[df.functions == 5]
        restaurantIndices = restaurantPoints.index[restaurantPoints.z == 0].values
        for i in restaurantIndices: 
            xneighbours = df[((df.x == (df.loc[i, 'x'] + 1)) | (df.x == (df.loc[i, 'x'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.z == (df.loc[i, 'z']))]
            yneighbours = df[((df.y == (df.loc[i, 'y'] + 1)) | (df.y == (df.loc[i, 'y'] - 1))) & (df.x == (df.loc[i, 'x'])) & (df.z == (df.loc[i, 'z']))]
            neighbours = pd.concat([xneighbours, yneighbours])
            candidates = neighbours[neighbours.functions == -1]
            acceptedCandidates = candidates[(candidates.shadowvalues <= maxShadowValueRestaurant) & (candidates.noisevalues >= minNoiseValueRestaurant)]
            mindist = 1000
            closestCandidate = firstRestaurantIndex
            for k in acceptedCandidates.index.values:
                dist = np.sqrt((df.loc[k, 'x'] - df.loc[firstAtriumIndex, 'x'])**2 + (df.loc[k, 'y'] - df.loc[firstAtriumIndex, 'y'])**2)
                if dist < mindist:
                    mindist = dist
                    closestCandidate = k
            df.loc[closestCandidate, 'functions'] = 5
            closestCandidate_z = df[(df.x == df.loc[closestCandidate, 'x']) & (df.y == df.loc[closestCandidate, 'y']) & (df.z == (df.loc[closestCandidate, 'z']+1))]
            df.loc[closestCandidate_z.index.values, 'functions'] = 5
            countaccepted = countaccepted + len(acceptedCandidates)
        if countaccepted == 0:
            restaurantFull = 1
            print('growing restaurant was interrupted because no acceptable voxels found')
    if (len(df[df.functions == 5])/2) >= maxSurfaceRestaurant:
        restaurantFull = 1


    if (len(df[df.functions == 6])/2) < maxSurfaceCinema:
        countaccepted = 0
        cinemaPoints = df[df.functions == 6]
        cinemaIndices = cinemaPoints.index[cinemaPoints.z == 0].values
        for i in cinemaIndices: 
            xneighbours = df[((df.x == (df.loc[i, 'x'] + 1)) | (df.x == (df.loc[i, 'x'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.z == (df.loc[i, 'z']))]
            yneighbours = df[((df.y == (df.loc[i, 'y'] + 1)) | (df.y == (df.loc[i, 'y'] - 1))) & (df.x == (df.loc[i, 'x'])) & (df.z == (df.loc[i, 'z']))]
            neighbours = pd.concat([xneighbours, yneighbours])
            candidates = neighbours[neighbours.functions == -1]
            acceptedCandidates = candidates[(candidates.shadowvalues <= maxShadowValueCinema) & (candidates.noisevalues >= minNoiseValueCinema)]
            mindist = 1000
            closestCandidate = firstCinemaIndex
            for k in acceptedCandidates.index.values:
                dist = np.sqrt((df.loc[k, 'x'] - df.loc[firstAtriumIndex, 'x'])**2 + (df.loc[k, 'y'] - df.loc[firstAtriumIndex, 'y'])**2)
                if dist < mindist:
                    mindist = dist
                    closestCandidate = k
            df.loc[closestCandidate, 'functions'] = 6
            closestCandidate_z = df[(df.x == df.loc[closestCandidate, 'x']) & (df.y == df.loc[closestCandidate, 'y']) & (df.z == (df.loc[closestCandidate, 'z']+1))]
            df.loc[closestCandidate_z.index.values, 'functions'] = 6
            countaccepted = countaccepted + len(acceptedCandidates)
        if countaccepted == 0:
            cinemaFull = 1
            print('growing cinema was interrupted because no acceptable voxels found')
    if (len(df[df.functions == 6])/2) >= maxSurfaceCinema:
        cinemaFull = 1


    if (len(df[df.functions == 7])/2) < maxSurfaceGym:
        countaccepted = 0
        gymPoints = df[df.functions == 7]
        gymIndices = gymPoints.index[gymPoints.z == 0].values
        for i in gymIndices:  
            xneighbours = df[((df.x == (df.loc[i, 'x'] + 1)) | (df.x == (df.loc[i, 'x'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.z == (df.loc[i, 'z']))]
            yneighbours = df[((df.y == (df.loc[i, 'y'] + 1)) | (df.y == (df.loc[i, 'y'] - 1))) & (df.x == (df.loc[i, 'x'])) & (df.z == (df.loc[i, 'z']))]
            neighbours = pd.concat([xneighbours, yneighbours])
            candidates = neighbours[neighbours.functions == -1]
            acceptedCandidates = candidates[(candidates.shadowvalues <= maxShadowValueGym) & (candidates.noisevalues >= minNoiseValueGym)]
            mindist = 1000
            closestCandidate = firstGymIndex
            for k in acceptedCandidates.index.values:
                dist = np.sqrt((df.loc[k, 'x'] - df.loc[firstAtriumIndex, 'x'])**2 + (df.loc[k, 'y'] - df.loc[firstAtriumIndex, 'y'])**2)
                if dist < mindist:
                    mindist = dist
                    closestCandidate = k
            df.loc[closestCandidate, 'functions'] = 7
            closestCandidate_z = df[(df.x == df.loc[closestCandidate, 'x']) & (df.y == df.loc[closestCandidate, 'y']) & (df.z == (df.loc[closestCandidate, 'z']+1))]
            df.loc[closestCandidate_z.index.values, 'functions'] = 7
            countaccepted = countaccepted + len(acceptedCandidates)
        if countaccepted == 0:
            gymFull = 1
            print('growing gym was interrupted because no acceptable voxels found')
    if (len(df[df.functions == 7])/2) >= maxSurfaceGym:
        gymFull = 1


    if (len(df[df.functions == 8])/2) < maxSurfaceSupermarket:
        countaccepted = 0
        supermarketPoints = df[df.functions == 8]
        supermarketIndices = supermarketPoints.index[supermarketPoints.z == 0].values
        for i in supermarketIndices:
            xneighbours = df[((df.x == (df.loc[i, 'x'] + 1)) | (df.x == (df.loc[i, 'x'] - 1))) & (df.y == (df.loc[i, 'y'])) & (df.z == (df.loc[i, 'z']))]
            yneighbours = df[((df.y == (df.loc[i, 'y'] + 1)) | (df.y == (df.loc[i, 'y'] - 1))) & (df.x == (df.loc[i, 'x'])) & (df.z == (df.loc[i, 'z']))]
            neighbours = pd.concat([xneighbours, yneighbours])
            candidates = neighbours[neighbours.functions == -1]
            acceptedCandidates = candidates[(candidates.shadowvalues <= maxShadowValueSupermarket) & (candidates.noisevalues >= minNoiseValueSupermarket)]
            mindist = 1000
            closestCandidate = firstSupermarketIndex
            for k in acceptedCandidates.index.values:
                dist = np.sqrt((df.loc[k, 'x'] - df.loc[firstAtriumIndex, 'x'])**2 + (df.loc[k, 'y'] - df.loc[firstAtriumIndex, 'y'])**2)
                if dist < mindist:
                    mindist = dist
                    closestCandidate = k
            df.loc[closestCandidate, 'functions'] = 8
            closestCandidate_z = df[(df.x == df.loc[closestCandidate, 'x']) & (df.y == df.loc[closestCandidate, 'y']) & (df.z == (df.loc[closestCandidate, 'z']+1))]
            df.loc[closestCandidate_z.index.values, 'functions'] = 8
            countaccepted = countaccepted + len(acceptedCandidates)
        if countaccepted == 0:
            supermarketFull = 1
            print('growing supermarket was interrupted because no acceptable voxels found')
    if (len(df[df.functions == 8])/2) >= maxSurfaceSupermarket:
        supermarketFull = 1

    counter = len(df[df.functions != -1]) #checks if there are still availbale points in the pointcloud

#deleting the atrium points above 4 floors as the functions around it don't grow above this level
indices = df.index[(df.functions == 0) & (df.z > 3)].values
df.loc[indices, 'functions'] = -1

#creating lists of the indexnumbers of the points in each function
indicesAtrium = []
indicesStudenthousing = []
indicesAssistedhousing = []
indicesStarterhousing = []
indicesWorkspacefunctions = []
indicesRestaurantfunctions = []
indicesCinemafunctions = []
indicesGymfunctions = []
indicesSupermarketfunctions = []

for i in df.index[df.functions == 0].values:
    indicesAtrium.append(i)
for i in df.index[df.functions == 1].values:
    indicesStudenthousing.append(i)
for i in df.index[df.functions == 2].values:
    indicesAssistedhousing.append(i)
for i in df.index[df.functions == 3].values:
    indicesStarterhousing.append(i)
for i in df.index[df.functions == 4].values:
    indicesWorkspacefunctions.append(i)
for i in df.index[df.functions == 5].values:
    indicesRestaurantfunctions.append(i)
for i in df.index[df.functions == 6].values:
    indicesCinemafunctions.append(i)
for i in df.index[df.functions == 7].values:
    indicesGymfunctions.append(i)
for i in df.index[df.functions == 8].values:
    indicesSupermarketfunctions.append(i)