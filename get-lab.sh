#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

END
#
#  Update a labtainers installation to use the latest tar and fetch the
#  latest baseline images
#
if [ "$#" -eq 1 ]; then
    echo $1
else
   echo " usage get-lab.sh lab-name"
   exit
fi
#
# figure out where we are executing from and go to the labtainer directory
#
here=`pwd`
if [[ $here == */labtainer ]]; then
   echo is at top >> /dev/null
elif [[ $here == */labtainer-student ]]; then
   #echo is in student
   real=`realpath ./`
   cd $real
   cd ../../..
elif [[ $here == */setup_scripts ]]; then
   cd ../../
else
   echo "Please run this script from the labtainer or labtainer-student directory"
   exit
fi


if [[ "$TEST_REGISTRY" != TRUE ]]; then
    #wget https://my.nps.edu/documents/107523844/109121513/labtainer.tar/6fc80410-e87d-4e47-ae24-cbb60c7619fa -O labtainer.tar
    #wget --quiet https://nps.box.com/shared/static/afz87ok8ezr0vtyo2qtlqbfmc28zk08j.tar -O labtainer.tar
    #wget --quiet https://github.com/mfthomps/Labtainers/raw/master/distrib/release/labtainer.tar -O labtainer.tar
   #  wget --quiet https://github.com/mfthomps/Labtainers/releases/latest/download/labtainer.tar -O labtainer.tar
    wget --quiet https://github.com/Ironem/LabsPFE/releases/latest/download/"$1".tgz -O "$1".tgz
    sync
else
    cp /media/sf_SEED/test_vms/$HOSTNAME/labtainer.tar .
    echo "USING SHARED FILE TAR, NOT PULLING FROM WEB"
    test_flag="-t"
fi


tar xf ./"$1".tgz --keep-newer-files --warning=none -C trunk/labs

# unzip -n -q ./labtainer/"$1".zip -d ./labtainer/trunk/labs/

rm ./"$1".tgz
