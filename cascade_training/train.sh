#!/bin/sh

vec=binary_description
info=positive_description.txt
bg=negative_description.txt
data=haarcascade_frontalcatface/
dst=../cascades/haarcascade_frontalcatface.xml

# Set numPosTotal to be the line count of info.
numPosTotal=`wc -l < $info`

# Set numNegTotal to be the line count of bg.
numNegTotal=`wc -l < $bg`

numPosPerStage=$(($numPosTotal*9/10))
numNegPerStage=$(($numNegTotal*9/10))
numStages=15
minHitRate=0.999

# Ensure that the data directory exists and is empty.
if [ ! -d "$data" ]; then
    mkdir "$data"
else
    rm "$data/*.xml"
fi

opencv_createsamples -vec "$vec" -info "$info" -bg "$bg" \
        -num "$numPosTotal"
opencv_traincascade -data "$data" -vec "$vec" -bg "$bg" \
        -numPos "$numPosPerStage" -numNeg "$numNegPerStage" \
        -numStages "$numStages" -minHitRate "$minHitRate"

cp "$data/cascade.xml" "$dst"