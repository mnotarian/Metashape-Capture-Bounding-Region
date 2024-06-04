#This script is designed to capture the bounding region of an open Metashape project 
#and export a new script that will apply the same region to other projects
#Other projects should be in the same CRS and the same geographic location
#The output script can be incorporated into a script that iteratively processes projects, too

import Metashape, os, glob

#File name must include *.py extension - this will add it if not typed in by user
file = Metashape.app.getSaveFileName("Save New Bounding Region Script as","",".py")
if not file:
    print("Script aborted")

if file[-3:].lower() != ".py":
    file += ".py"

#capture the bounding region of the open project
T0 = Metashape.app.document.chunk.transform.matrix
T01 = str([T0[0,0], T0[0,1], T0[0,2], T0[0,3]])
T02 = str([T0[1,0], T0[1,1], T0[1,2], T0[1,3]])
T03 = str([T0[2,0], T0[2,1], T0[2,2], T0[2,3]])
T04 = str([T0[3,0], T0[3,1], T0[3,2], T0[3,3]])
region = Metashape.app.document.chunk.region
R0 = region.rot
R01 = str([R0[0,0], R0[0,1], R0[0,2]])
R02 = str([R0[1,0], R0[1,1], R0[1,2]])
R03 = str([R0[2,0], R0[2,1], R0[2,2]])
C0 = region.center
C0 = str([C0[0],C0[1],C0[2]])
s0 = region.size
s0 = str([s0[0],s0[1],s0[2]])

#write the new script as a long string
content = ("import Metashape, os, glob\n\nT0 = Metashape.Matrix([%s,%s,%s,%s])\nT = Metashape.app.document.chunk.transform.matrix.inv() * T0\n\nR = Metashape.Matrix([[T[0, 0], T[0, 1], T[0, 2]],[T[1, 0], T[1, 1], T[1, 2]], [T[2, 0], T[2, 1], T[2, 2]]])\n\nscale = R.row(0).norm()\nR = R * (1 / scale)\n\nR0 = Metashape.Matrix([%s,%s,%s])\n\nnew_region = Metashape.Region()\nnew_region.rot = R * R0\nc = T.mulp(Metashape.Vector(%s))\nnew_region.center = c\nnew_region.size = Metashape.Vector(%s) * scale / 1.\n\nMetashape.app.document.chunk.region = new_region" % (T01, T02, T03, T04, R01, R02, R03, C0, s0))

#export the new script file
with open(file, 'w') as script:
  script.writelines(content)

print("Success!")
print("Script exported to: ",file)