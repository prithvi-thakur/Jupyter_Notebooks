#!bin/bash

# Central-Southern California map
#

# Add preferences here
#gmt gmtset MAP_FRAME_PEN 3

gmtset FORMAT_GEO_MAP DD #set labels on the map to decimal degrees

gmtset MAP_FRAME_TYPE fancy #make outline of the map a single line with ticks

gmtset FONT_TITLE 24p #size of the title font

gmtset MAP_TITLE_OFFSET -0.4c #offset the map title down by 0.4 cm

gmtset FONT_LABEL 14p #size of the label fonts

gmtset MAP_LABEL_OFFSET 0.3c #offset the labels up by 0.3 cm

gmtset FONT_ANNOT_PRIMARY 12p #size of the primary annotation font

#set the -R flag: LONleft/LONright/ LATbottom/ LATtop
region="-R-121.30/-120.10/35.70/36.70"

#set the -J flag:
#-JM6i= mercator projection with longest axis=6 inches
#-JX7i/2i= XY projection 7 inches horizontal and 2 inches vertical
#
projection="-JM5i"

#used with the opening/first postscript file
open="-K -V"

#used when adding to an existing postscript file
add="-O -K -V"

#used when adding the last object to postscript file
close="-O -V"

#output file names
psFile=$1.ps

pdfFile=$1.pdf

#topo file
topo=../GMRTv3_7_20191217topo.grd

# gps file
gps_vel=../gps/cwu.snaps_nam08.vel

#Start code here
misc="-X2.5 -Y5"
psbasemap $region $projection -P -B0.5/0.5WSen $misc $open > $psFile

#make color pallete
makecpt -Cetopo1 -T-7000/7000/500 -Z > topo.cpt

# create gradient file
grdgradient $topo -A135 -Ne0.5 -Gshadow.grd

grdimage $topo $region $projection $add -Ctopo.cpt -Ishadow.grd >> $psFile

# Use this for topography
pscoast $region $projection $add -Wthinnest -Df -Na >> $psFile

# Use this for simple colored map
# pscoast $region $projection $add -Wthinnest -Slightblue -Gtan -Df -I1 -Na >> $psFile

# Add San Benito and Parkfield to the map
psxy $region $projection $add -Sc0.3 -Gblack << END >> $psFile
-120.435226 35.895191
-121.082230 36.509760
END
pstext $region $projection $add  -Y-0.2 << END >> $psFile
-120.435226 35.895191 14 0 1 CT Parkfield
-121.082230 36.509760 14 0 1 CT San Benito
END

# Draw San Andreas Fault
psxy $region $projection $add -GBrown -A -Wthick << END >> $psFile
-120.435226 35.895191
-121.082230 36.509760
END

# Plot GPS velocities
# awk 'NR>37 {print ($9-360),$8,$21,$20,$24,$23,$26,$1}' $gps_vels | psvelo $region $projection -Se0.05/0.95/0 -W.3p,100 -A10p+e -Gblue $add >> $psFile  # 205/133/63.

# awk 'NR>37 {print ($9-360),$8,$21,$20,$24,$23,$26,$1}' $gps_vels | psvelo $region $projection -Se0.05/0/0 -W2p,blue -A10p+e -Gblue $add >> $psFile  # 205/133/63.


rm temp_test.dat
awk 'NR>37 {print $9-360,$8,$21,$20,$24,$23,$26, $1}' ../gps_data/cwu.snaps_nam08.vel > temp_test.dat

tmp=temp_test.dat
psvelo $tmp $region $projection $add -Se0.05/0.95/0 -W1p -A5p+e -Gblue >> $psFile
psvelo $tmp $region $projection $add -Se50/0.95/0 -W1p,blue -A5p+e -Gblue >> $psFile



ps2pdf $psFile $pdfFile
open $pdfFile
echo "end of script"

