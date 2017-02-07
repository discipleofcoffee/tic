#!/usr/bin/env bash 

echo "==========================="
echo "Creating Compressed Tarball"
echo

cencParticipant 

mkdir ${cencParticipant}
cd ${cencParticipant}
ln -s ../20* .

cd ..
tar -hzcvf ${cencParticipant}.tar.gz  ${cencParticipant}

rm -rf ${cencParticipant}