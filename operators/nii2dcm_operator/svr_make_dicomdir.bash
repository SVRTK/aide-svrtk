#!/bin/bash

### svr_make_dicomdir
#
# - creates DICOMDIR, moves alongside DICOM folder
# - nb: very hacky because originally for Windows - should be able to integrate into application.py
#
# Requires:
# - dcmtk
#
# Tom Roberts (t.roberts@kcl.ac.uk)
#
###########################################################

echo
echo "Creating DICOMDIR ..."

# prideDir=/mnt/c/svrtk-docker-gpu/recon/pride # local paths
prideDir=/home/recon/pride # container paths

mkdir $prideDir/TempOutputSeries/tempDir
mv $prideDir/TempOutputSeries/DICOM $prideDir/TempOutputSeries/tempDir/DICOM
cd $prideDir/TempOutputSeries
/usr/bin/dcmmkdir +id 'tempDir' +r
mv $prideDir/TempOutputSeries/tempDir/DICOM $prideDir/TempOutputSeries
rm -r tempDir

echo "DICOMDIR created."
echo