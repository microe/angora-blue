#!/bin/sh

wget http://137.189.35.203/WebUI/CatDatabase/Data/CAT_DATASET_01.zip
wget http://137.189.35.203/WebUI/CatDatabase/Data/CAT_DATASET_02.zip
wget http://www.vision.caltech.edu/Image_Datasets/faces/faces.tar
wget http://pascallin.ecs.soton.ac.uk/challenges/VOC/voc2007/VOCtest_06-Nov-2007.tar
unzip *.zip
tar -xvf *.tar