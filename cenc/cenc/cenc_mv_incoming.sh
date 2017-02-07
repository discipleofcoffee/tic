#!/usr/bin/env bash 

cencDir=/cenc/mri/subjects/
cencParticipant=${1:0:7}
cencParticipantDir=${cencDir}/${cencParticipant}

echo "Making directory ${cencParticipantDir}/data"

mkdir -p ${cencParticipantDir}/data/

echo "==========================="
echo "Moving data from $1 to $2"
echo
mv -v $1 ${cencParticipantDir}/data/dicom

echo "==========================="
echo "Creating Compressed Tarball"
echo

cd ${cencParticipantDir}/data/dicom

mkdir ${cencParticipant}
cd ${cencParticipant}
ln -s ../20* .

cd ..
tar -hzcvf ${cencParticipant}.tar.gz  ${cencParticipant}

rm -rf ${cencParticipant}