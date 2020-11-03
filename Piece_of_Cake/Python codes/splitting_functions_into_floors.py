import rhinoscriptsyntax as rs

bg = []
eerste = []
tweede = []
derde = []
vierde = []
vijfde = []
zesde = []
zevende = []
achtste = []
negende = []
tiende = []

HalfHeight = Height/2

for i in range(0,len(Distances)):
    if Distances[i] < HalfHeight:
        bg.append(AllPoints[i])
    if HalfHeight < Distances[i] < (Height + HalfHeight):
        eerste.append(AllPoints[i])
    if (Height + HalfHeight) < Distances[i] < (Height*2 + HalfHeight):
        tweede.append(AllPoints[i])
    if (Height*2 + HalfHeight) < Distances[i] < (Height*3 + HalfHeight):
        derde.append(AllPoints[i])
    if (Height*3 + HalfHeight) < Distances[i] < (Height*4 + HalfHeight):
        vierde.append(AllPoints[i])
    if (Height*4 + HalfHeight) < Distances[i] < (Height*5 + HalfHeight):
        vijfde.append(AllPoints[i])
    if (Height*5 + HalfHeight) < Distances[i] < (Height*6 + HalfHeight):
        zesde.append(AllPoints[i])
    if (Height*6 + HalfHeight) < Distances[i] < (Height*7 + HalfHeight):
        zevende.append(AllPoints[i])
    if (Height*7 + HalfHeight) < Distances[i] < (Height*8 + HalfHeight):
        achtste.append(AllPoints[i])
    if (Height*8 + HalfHeight) < Distances[i] < (Height*9 + HalfHeight):
        negende.append(AllPoints[i])