import copy
import csv
import math
import random
import numpy as np
from scipy.spatial import distance


class gridpoint:
    def __init__(self, x, y, z, height,noisedist,courtdist,vijvdist):
        self.x = x
        self.y = y
        self.z = z
        self.h = height
        self.n = noisedist
        self.c = courtdist
        self.v = vijvdist

class cluster:
    def __init__(self,name,voxels,hfac,nfac,courtfac,vijvfac):
        self.name = name
        self.voxels = voxels
        self.hfac = hfac
        self.nfac = nfac
        self.courtfac = courtfac
        self.vijvfac = vijvfac

def grower(growth,scoreslist,closest6,voxels,growptlist): 
    for i in range(len(growth)):
        if len(growth) >= voxels: # if voxels is reached break out of function, otherwise end loop then call function again
            break
        pt = growth[i]
        nghbrs = []
        for j in range(len(closest6[pt])):   #add useable neighbours to list of neighbours
            if closest6[growth[i]][j] != len(Grid)+10:
                nghbrs.append(closest6[pt][j])
            
        #if there's no neighbours left, dont add a point to the growth\
        
        if (len(nghbrs) == 0) or (nghbrs[0] == len(Grid)+10) :
            continue
        
        newscorelist = []
        for j in range(len(nghbrs)) : #put scores of neighbours in a list
            newscorelist.append(scoreslist[nghbrs[j]])

        index_maxscore2 = max(xrange(len(newscorelist)), key=newscorelist.__getitem__) #finds index of max score
        if scoreslist[nghbrs[index_maxscore2]] == -1000:    #Skip points that are deemed unuseable
            continue
        growth.append(nghbrs[index_maxscore2])          #Put index of point in growth
    
        scoreslist[nghbrs[index_maxscore2]] = 0 #sets score of choses point to 0
        growptlist[nghbrs[index_maxscore2]].h = 0
        growptlist[nghbrs[index_maxscore2]].n = 0


        for j in range(len(closest6)):          #sets the chosen point to an arbitrary value in the neighbourhood list
            for k in range(len(closest6[j])):
                if closest6[j][k] == nghbrs[index_maxscore2]:
                    closest6[j][k] = len(Grid)+10
        if len(growth) >= voxels: # if voxels is reached break out of function, otherwise end loop then call function again
            break
        else:
            growth = grower(growth,scoreslist,closest6,voxels,growptlist)
        
        
    return growth
       
def zerolistmaker(n): #makes a list of zeroes, used in places where the length of the list is known, to reduce memory reads & writes
    listofzeros = [0] * n
    return listofzeros

###############################################################################################################

#define clustersize

startersize = 225
studenthsize = 75
elderlysize = 125
worksize = 226
studentfsize = 11
daysize = 50
librarysize = 16
cinemasize = 35

#Percentage of required voxels that will grow
Growfactor = Percent

#define clusterfactors
#hfac: negative = lower, positive = heigher
#nfac: negative = closer to noisepoint, positive = farther from noisepoint
#courtfac: negative = closer to courtyard, positive = farther from courtyard
#vijvfac: negative = closer to vijverhofpoint, positive = farther from vijverhofpoint

starterhfac = 0.7
starternfac = 0.5
startercourtfac = -0.2
startervijvfac = -0.3


studenthhfac = 0.6
studenthnfac = 0.3
studenthcourtfac = -0.2
studenthvijvfac = 0


elderlyhfac = -1
elderlynfac = 0.8
elderlycourtfac = -0.8
elderlyvijvfac = -0.4


workhfac = -0.1
worknfac = -0.8
workcourtfac = -0.3
workvijvfac = 0


studentfhfac = -1
studentfnfac = 0.1
studentfcourtfac = -0.3
studentfvijvfac = 0


dayhfac = -1
daynfac = 0.1
daycourtfac = -0.3
dayvijvfac = 0


libraryhfac = -0.6
librarynfac = 0.7
librarycourtfac = 0
libraryvijvfac = 0

cinemahfac = -0.6
cinemanfac = 0.7
cinemacourtfac = 0
cinemavijvfac = 0




#create clusters
starters = cluster('STARTERS', int(math.ceil(startersize*(Growfactor/10))), starterhfac,starternfac, startercourtfac, startervijvfac)
studenth = cluster('STUDENTHOUSING', int(math.ceil(studenthsize*(Growfactor/10))), studenthhfac,studenthnfac, studenthcourtfac, studenthvijvfac)
elderly = cluster('ELDERLY', int(math.ceil(elderlysize*(Growfactor/10))), elderlyhfac,elderlynfac, elderlycourtfac, elderlyvijvfac)
work = cluster( 'WORK', int(math.ceil(worksize*(Growfactor/10))), workhfac,worknfac, workcourtfac, workvijvfac)
studentf = cluster('STUDENTFREETIME', int(math.ceil(studentfsize*(Growfactor/10))), studentfhfac,studentfnfac, studentfcourtfac, studentfvijvfac)
day = cluster('DAYTODAY', int(math.ceil(daysize*(Growfactor/10))), dayhfac,daynfac, daycourtfac, dayvijvfac)
library = cluster('LIBRARY', int(math.ceil(librarysize*(Growfactor/10))), libraryhfac, librarynfac, librarycourtfac, libraryvijvfac)
cinema = cluster('CINEMA', int(math.ceil(cinemasize*(Growfactor/10))), cinemahfac, cinemanfac, cinemacourtfac, cinemavijvfac)


###############################################################################################################
#Pre Growing computation (normalized height and distance from noisepoint, neighbours) Starting Points?

growptlist = zerolistmaker(len(Grid)) #starts list of gridpoints
heightlist = zerolistmaker(len(Grid))
noisedistlist = zerolistmaker(len(Grid))
courtdistlist = zerolistmaker(len(Grid))
vijvdistlist = zerolistmaker(len(Grid))
for i in range(len(Grid)):
    heightlist[i] = Grid[i][2]
    noisedistlist[i] = (Grid[i][0]-NoisePoint[0])**2+(Grid[i][1]-NoisePoint[1])**2+(Grid[i][2]-NoisePoint[2])**2
    courtdistlist[i] = (Grid[i][0]-CourtPoint[0])**2+(Grid[i][1]-CourtPoint[1])**2+(Grid[i][2]-CourtPoint[2])**2
    vijvdistlist[i] = (Grid[i][0]-VijvPoint[0])**2+(Grid[i][1]-VijvPoint[1])**2+(Grid[i][2]-VijvPoint[2])**2


# find max values for normalization    
maxheight = max(heightlist)
maxnoisedist = max(noisedistlist)
maxcourtdist = max(courtdistlist)
maxvijvdist = max(vijvdistlist)


for i in range(len(Grid)): #makes a gridpoint to grow on for each point in Grid
    normalheight = ((Grid[i][2]/maxheight)+0.01) #height / largest height in grid
    normalnoise =   noisedistlist[i]/maxnoisedist#distance to noisepoint / largest distance from noisepoint in Grid
    normalcourt =   courtdistlist[i]/maxcourtdist#distance to courtpoint / largest distance from courtpoint in Grid
    normalvijv =   vijvdistlist[i]/maxvijvdist#distance to vijvpoint / largest distance from vijvpoint in Grid
    growpt = gridpoint(Grid[i][0],Grid[i][1],Grid[i][2],normalheight,normalnoise,normalcourt,normalvijv)
    growptlist[i] = growpt



D = distance.squareform(distance.pdist(Grid))
  # For each point, find the to all of the other points.
closest = np.argsort(D, axis=1)     
k = 6  # For each point, find the k closest points
closest6 = (closest[:, 1:k+1])
for i in range(len(closest6)):          #sets the points that arent direct neighbours to an arbitrary value
    for j in range(len(closest6[i])):
        if D[i][closest6[i][j]] > 5.1:
            closest6[i][j] = len(Grid)+10

orderlist = []  #list to output later to show the hierarchy used when placing the clusters
result = []      #list used to check if the growing was succesfull, if it failed, it will show where
rempoints = len(Grid)    #shows remaining amount of points
########################################################################################################
#GROWING
#Growing is the same for every cluster except the elderly cluster (they avoid the ground floor)

##Growing starters



newclust = starters   #sets current cluster


tempgrowptlist = growptlist   #stores growptlist so grower can try multiple times

scoreslist = zerolistmaker(len(Grid)) #start/reset list of scores for this cluster (as long as gridpointlist)
for i in range(len(growptlist)): #computes score for each point
    if (growptlist[i].h ==0) or (growptlist[i].n ==0):  #skips points that were previously used (might be redundant)
        score = -1000
    else:
        score = newclust.hfac*growptlist[i].h+newclust.nfac*growptlist[i].n+newclust.courtfac*growptlist[i].c+newclust.vijvfac*growptlist[i].v
        #the score is the sum of every factor times its respective attribute
    scoreslist[i] = score
tempscoreslist = scoreslist #stores scoreslist so grower can try multiple times
startscoreslist = scoreslist    #stores scoreslist so grower can try multiple times
growth = [] # start growth list
growth2 = [] #needs to be defined before entering loop


growtimer = 0   #timer to avoid recursion
while (len(growth2)<newclust.voxels): #loops as long as desired amount of voxels is not reached
    if growtimer >rempoints: #condition to stop recursion
        result.append("FAIL " + (str(newclust.name)))
        break
    scoreslist = tempscoreslist
    growtimer = growtimer +1
    index_maxscore1 = max(xrange(len(startscoreslist)), key=startscoreslist.__getitem__)    #gets index of highest score
    growth = [] #start/reset growth list
    growth2 = [] #second growth so grower can try multiple times
    growth.append(index_maxscore1)    #puts index with highest score in growth list
    scoreslist[index_maxscore1] = -1000
    startscoreslist[index_maxscore1] = -1000
    growptlist[index_maxscore1].h = 0
    growptlist[index_maxscore1].n = 0

    growth2 = grower(growth,scoreslist,closest6,newclust.voxels,growptlist)
    
    
for i in range(len(growth2)):  #sets points of first useable combination of voxels to unuseable
    tempgrowptlist[growth2[i]].h = 0
    tempgrowptlist[growth2[i]].n = 0

growptlist = tempgrowptlist

templist = zerolistmaker(len(growth2))
for i in range(len(growth2)): #appends chosen points to a list
    templist[i] = Grid[growth2[i]]
orderlist.append(newclust.name)

startersP = templist

rempoints = rempoints - len(templist)



##Growing Student Housing

newclust = studenth #sets current cluster


tempgrowptlist = growptlist   #stores growptlist so grower can try multiple times

scoreslist = zerolistmaker(len(Grid)) #start/reset list of scores for this cluster (as long as gridpointlist)
for i in range(len(growptlist)): #computes score for each point
    if (growptlist[i].h ==0) or (growptlist[i].n ==0):  #skips points that were previously used (might be redundant)
        score = -1000
    else:
        score = newclust.hfac*growptlist[i].h+newclust.nfac*growptlist[i].n+newclust.courtfac*growptlist[i].c+newclust.vijvfac*growptlist[i].v
        #the score is the sum of every factor times its respective attribute
    scoreslist[i] = score
tempscoreslist = scoreslist #stores scoreslist so grower can try multiple times
startscoreslist = scoreslist    #stores scoreslist so grower can try multiple times
growth = [] # start growth list
growth2 = [] #needs to be defined before entering loop


growtimer = 0   #timer to avoid recursion
while (len(growth2)<newclust.voxels): #loops as long as desired amount of voxels is not reached
    if growtimer >rempoints: #condition to stop recursion
        result.append("FAIL " + (str(newclust.name)))
        break
    scoreslist = tempscoreslist
    growtimer = growtimer +1
    index_maxscore1 = max(xrange(len(startscoreslist)), key=startscoreslist.__getitem__)    #gets index of highest score
    growth = [] #start/reset growth list
    growth2 = [] #second growth so grower can try multiple times
    growth.append(index_maxscore1)    #puts index with highest score in growth list
    scoreslist[index_maxscore1] = -1000
    startscoreslist[index_maxscore1] = -1000
    growptlist[index_maxscore1].h = 0
    growptlist[index_maxscore1].n = 0

    growth2 = grower(growth,scoreslist,closest6,newclust.voxels,growptlist)
    
    
for i in range(len(growth2)):  #sets points of first useable combination of voxels to unuseable
    tempgrowptlist[growth2[i]].h = 0
    tempgrowptlist[growth2[i]].n = 0

growptlist = tempgrowptlist

templist = zerolistmaker(len(growth2))
for i in range(len(growth2)): #appends chosen points to a list
    templist[i] = Grid[growth2[i]]
orderlist.append(newclust.name)







studenthP = templist
rempoints = rempoints - len(templist)
##Growing work

newclust = work #sets current cluster


tempgrowptlist = growptlist   #stores growptlist so grower can try multiple times

scoreslist = zerolistmaker(len(Grid)) #start/reset list of scores for this cluster (as long as gridpointlist)
for i in range(len(growptlist)): #computes score for each point
    if (growptlist[i].h ==0) or (growptlist[i].n ==0):  #skips points that were previously used (might be redundant)
        score = -1000
    else:
        score = newclust.hfac*growptlist[i].h+newclust.nfac*growptlist[i].n+newclust.courtfac*growptlist[i].c+newclust.vijvfac*growptlist[i].v
        #the score is the sum of every factor times its respective attribute
    scoreslist[i] = score
tempscoreslist = scoreslist #stores scoreslist so grower can try multiple times
startscoreslist = scoreslist    #stores scoreslist so grower can try multiple times
growth = [] # start growth list
growth2 = [] #needs to be defined before entering loop


growtimer = 0   #timer to avoid recursion
while (len(growth2)<newclust.voxels): #loops as long as desired amount of voxels is not reached
    if growtimer >rempoints: #condition to stop recursion
        result.append("FAIL " + (str(newclust.name)))
        break
    scoreslist = tempscoreslist
    growtimer = growtimer +1
    index_maxscore1 = max(xrange(len(startscoreslist)), key=startscoreslist.__getitem__)    #gets index of highest score
    growth = [] #start/reset growth list
    growth2 = [] #second growth so grower can try multiple times
    growth.append(index_maxscore1)    #puts index with highest score in growth list
    scoreslist[index_maxscore1] = -1000
    startscoreslist[index_maxscore1] = -1000
    growptlist[index_maxscore1].h = 0
    growptlist[index_maxscore1].n = 0

    growth2 = grower(growth,scoreslist,closest6,newclust.voxels,growptlist)
    
    
for i in range(len(growth2)):  #sets points of first useable combination of voxels to unuseable
    tempgrowptlist[growth2[i]].h = 0
    tempgrowptlist[growth2[i]].n = 0

growptlist = tempgrowptlist

templist = zerolistmaker(len(growth2))
for i in range(len(growth2)): #appends chosen points to a list
    templist[i] = Grid[growth2[i]]
orderlist.append(newclust.name)








workP = templist
rempoints = rempoints - len(templist)



##Growing elderly!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

newclust = elderly #sets current cluster


tempgrowptlist = growptlist   #stores growptlist


scoreslist = zerolistmaker(len(Grid)) #start/reset list of scores (as long as gridpointlist)
for i in range(len(growptlist)): #computes score for each point
    if (growptlist[i].h ==0) or (growptlist[i].n ==0):
        score = -1000
    elif (heightlist[i]<3.0): #sets points that are below the 1st floor to unuseable!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        score = -1000
    else:
        score = newclust.hfac*growptlist[i].h+newclust.nfac*growptlist[i].n+newclust.courtfac*growptlist[i].c+newclust.vijvfac*growptlist[i].v
    scoreslist[i] = score
tempscoreslist = scoreslist
startscoreslist = scoreslist

index_maxscore1 = max(xrange(len(scoreslist)), key=scoreslist.__getitem__)    #gets index of highest score
for i in range(len(closest6)):          #sets the starting point to an arbitrary value
    for j in range(len(closest6[i])):
        if closest6[i][j] == index_maxscore1:
                    closest6[i][j] = len(Grid)+10
growth = [] #start/reset growth list
growth2 = []
growtimer = 0
while (len(growth2)<newclust.voxels):
    if growtimer >rempoints:
        result.append("FAIL " + (str(newclust.name)))
        break
    scoreslist = tempscoreslist
    growtimer = growtimer +1
    index_maxscore1 = max(xrange(len(startscoreslist)), key=startscoreslist.__getitem__)    #gets index of highest score
    growth = [] #start/reset growth list
    growth2 = []
    growth.append(index_maxscore1)    #puts index with highest score in growth list
    scoreslist[index_maxscore1] = -1000
    startscoreslist[index_maxscore1] = -1000
    growptlist[index_maxscore1].h = 0
    growptlist[index_maxscore1].n = 0

    growth2 = grower(growth,scoreslist,closest6,newclust.voxels,growptlist)
    
    
for i in range(len(growth2)):
    tempgrowptlist[growth2[i]].h = 0
    tempgrowptlist[growth2[i]].n = 0

growptlist = tempgrowptlist

templist = zerolistmaker(len(growth2))
for i in range(len(growth2)):
    templist[i] = Grid[growth2[i]]
orderlist.append(newclust.name)




elderlyP = templist
rempoints = rempoints - len(templist)



##Growing student free time

newclust = studentf #sets current cluster


tempgrowptlist = growptlist   #stores growptlist so grower can try multiple times

scoreslist = zerolistmaker(len(Grid)) #start/reset list of scores for this cluster (as long as gridpointlist)
for i in range(len(growptlist)): #computes score for each point
    if (growptlist[i].h ==0) or (growptlist[i].n ==0):  #skips points that were previously used (might be redundant)
        score = -1000
    else:
        score = newclust.hfac*growptlist[i].h+newclust.nfac*growptlist[i].n+newclust.courtfac*growptlist[i].c+newclust.vijvfac*growptlist[i].v
        #the score is the sum of every factor times its respective attribute
    scoreslist[i] = score
tempscoreslist = scoreslist #stores scoreslist so grower can try multiple times
startscoreslist = scoreslist    #stores scoreslist so grower can try multiple times
growth = [] # start growth list
growth2 = [] #needs to be defined before entering loop


growtimer = 0   #timer to avoid recursion
while (len(growth2)<newclust.voxels): #loops as long as desired amount of voxels is not reached
    if growtimer >rempoints: #condition to stop recursion
        result.append("FAIL " + (str(newclust.name)))
        break
    scoreslist = tempscoreslist
    growtimer = growtimer +1
    index_maxscore1 = max(xrange(len(startscoreslist)), key=startscoreslist.__getitem__)    #gets index of highest score
    growth = [] #start/reset growth list
    growth2 = [] #second growth so grower can try multiple times
    growth.append(index_maxscore1)    #puts index with highest score in growth list
    scoreslist[index_maxscore1] = -1000
    startscoreslist[index_maxscore1] = -1000
    growptlist[index_maxscore1].h = 0
    growptlist[index_maxscore1].n = 0

    growth2 = grower(growth,scoreslist,closest6,newclust.voxels,growptlist)
    
    
for i in range(len(growth2)):  #sets points of first useable combination of voxels to unuseable
    tempgrowptlist[growth2[i]].h = 0
    tempgrowptlist[growth2[i]].n = 0

growptlist = tempgrowptlist

templist = zerolistmaker(len(growth2))
for i in range(len(growth2)): #appends chosen points to a list
    templist[i] = Grid[growth2[i]]
orderlist.append(newclust.name)




studentfP = templist
rempoints = rempoints - len(templist)


##Growing library

newclust = library #sets current cluster


tempgrowptlist = growptlist   #stores growptlist so grower can try multiple times

scoreslist = zerolistmaker(len(Grid)) #start/reset list of scores for this cluster (as long as gridpointlist)
for i in range(len(growptlist)): #computes score for each point
    if (growptlist[i].h ==0) or (growptlist[i].n ==0):  #skips points that were previously used (might be redundant)
        score = -1000
    else:
        score = newclust.hfac*growptlist[i].h+newclust.nfac*growptlist[i].n+newclust.courtfac*growptlist[i].c+newclust.vijvfac*growptlist[i].v
        #the score is the sum of every factor times its respective attribute
    scoreslist[i] = score
tempscoreslist = scoreslist #stores scoreslist so grower can try multiple times
startscoreslist = scoreslist    #stores scoreslist so grower can try multiple times
growth = [] # start growth list
growth2 = [] #needs to be defined before entering loop


growtimer = 0   #timer to avoid recursion
while (len(growth2)<newclust.voxels): #loops as long as desired amount of voxels is not reached
    if growtimer >rempoints: #condition to stop recursion
        result.append("FAIL " + (str(newclust.name)))
        break
    scoreslist = tempscoreslist
    growtimer = growtimer +1
    index_maxscore1 = max(xrange(len(startscoreslist)), key=startscoreslist.__getitem__)    #gets index of highest score
    growth = [] #start/reset growth list
    growth2 = [] #second growth so grower can try multiple times
    growth.append(index_maxscore1)    #puts index with highest score in growth list
    scoreslist[index_maxscore1] = -1000
    startscoreslist[index_maxscore1] = -1000
    growptlist[index_maxscore1].h = 0
    growptlist[index_maxscore1].n = 0

    growth2 = grower(growth,scoreslist,closest6,newclust.voxels,growptlist)
    
    
for i in range(len(growth2)):  #sets points of first useable combination of voxels to unuseable
    tempgrowptlist[growth2[i]].h = 0
    tempgrowptlist[growth2[i]].n = 0

growptlist = tempgrowptlist

templist = zerolistmaker(len(growth2))
for i in range(len(growth2)): #appends chosen points to a list
    templist[i] = Grid[growth2[i]]
orderlist.append(newclust.name)





libraryP = templist
rempoints = rempoints - len(templist)


##Growing Cinema

newclust = cinema #sets current cluster


tempgrowptlist = growptlist   #stores growptlist so grower can try multiple times

scoreslist = zerolistmaker(len(Grid)) #start/reset list of scores for this cluster (as long as gridpointlist)
for i in range(len(growptlist)): #computes score for each point
    if (growptlist[i].h ==0) or (growptlist[i].n ==0):  #skips points that were previously used (might be redundant)
        score = -1000
    else:
        score = newclust.hfac*growptlist[i].h+newclust.nfac*growptlist[i].n+newclust.courtfac*growptlist[i].c+newclust.vijvfac*growptlist[i].v
        #the score is the sum of every factor times its respective attribute
    scoreslist[i] = score
tempscoreslist = scoreslist #stores scoreslist so grower can try multiple times
startscoreslist = scoreslist    #stores scoreslist so grower can try multiple times
growth = [] # start growth list
growth2 = [] #needs to be defined before entering loop


growtimer = 0   #timer to avoid recursion
while (len(growth2)<newclust.voxels): #loops as long as desired amount of voxels is not reached
    if growtimer >rempoints: #condition to stop recursion
        result.append("FAIL " + (str(newclust.name)))
        break
    scoreslist = tempscoreslist
    growtimer = growtimer +1
    index_maxscore1 = max(xrange(len(startscoreslist)), key=startscoreslist.__getitem__)    #gets index of highest score
    growth = [] #start/reset growth list
    growth2 = [] #second growth so grower can try multiple times
    growth.append(index_maxscore1)    #puts index with highest score in growth list
    scoreslist[index_maxscore1] = -1000
    startscoreslist[index_maxscore1] = -1000
    growptlist[index_maxscore1].h = 0
    growptlist[index_maxscore1].n = 0

    growth2 = grower(growth,scoreslist,closest6,newclust.voxels,growptlist)
    
    
for i in range(len(growth2)):  #sets points of first useable combination of voxels to unuseable
    tempgrowptlist[growth2[i]].h = 0
    tempgrowptlist[growth2[i]].n = 0

growptlist = tempgrowptlist

templist = zerolistmaker(len(growth2))
for i in range(len(growth2)): #appends chosen points to a list
    templist[i] = Grid[growth2[i]]
orderlist.append(newclust.name)



cinemaP = templist
rempoints = rempoints - len(templist)
##Growing day to day

newclust = day #sets current cluster


tempgrowptlist = growptlist   #stores growptlist so grower can try multiple times

scoreslist = zerolistmaker(len(Grid)) #start/reset list of scores for this cluster (as long as gridpointlist)
for i in range(len(growptlist)): #computes score for each point
    if (growptlist[i].h ==0) or (growptlist[i].n ==0):  #skips points that were previously used (might be redundant)
        score = -1000
    else:
        score = newclust.hfac*growptlist[i].h+newclust.nfac*growptlist[i].n+newclust.courtfac*growptlist[i].c+newclust.vijvfac*growptlist[i].v
        #the score is the sum of every factor times its respective attribute
    scoreslist[i] = score
tempscoreslist = scoreslist #stores scoreslist so grower can try multiple times
startscoreslist = scoreslist    #stores scoreslist so grower can try multiple times
growth = [] # start growth list
growth2 = [] #needs to be defined before entering loop


growtimer = 0   #timer to avoid recursion
while (len(growth2)<newclust.voxels): #loops as long as desired amount of voxels is not reached
    if growtimer >rempoints: #condition to stop recursion
        result.append("FAIL " + (str(newclust.name)))
        break
    scoreslist = tempscoreslist
    growtimer = growtimer +1
    index_maxscore1 = max(xrange(len(startscoreslist)), key=startscoreslist.__getitem__)    #gets index of highest score
    growth = [] #start/reset growth list
    growth2 = [] #second growth so grower can try multiple times
    growth.append(index_maxscore1)    #puts index with highest score in growth list
    scoreslist[index_maxscore1] = -1000
    startscoreslist[index_maxscore1] = -1000
    growptlist[index_maxscore1].h = 0
    growptlist[index_maxscore1].n = 0

    growth2 = grower(growth,scoreslist,closest6,newclust.voxels,growptlist)
    
    
for i in range(len(growth2)):  #sets points of first useable combination of voxels to unuseable
    tempgrowptlist[growth2[i]].h = 0
    tempgrowptlist[growth2[i]].n = 0

growptlist = tempgrowptlist

templist = zerolistmaker(len(growth2))
for i in range(len(growth2)): #appends chosen points to a list
    templist[i] = Grid[growth2[i]]
orderlist.append(newclust.name)




dayP = templist
rempoints = rempoints - len(templist)
#################################################################################################
#sets output variable to correct values
order = orderlist
if len(result) > 0:
    check = result
else:
    check = 'Success!'

Remaining = rempoints
