#!/bin/bash
#
# Create a master Labtainer image for use in running Labtainers from a container
# on any system that has Docker installed, withou having to install Labtainers.
# Thanks to Olivier Berger and Allen Harper for this contribution.
#
here=`pwd`
cd ../
mkdir -p workspace_master
rm -fr workspace_master/*
cp -a $LABTAINER_DIR/headless-lite/Dockerfile.labtainer.master.headless workspace_master/Dockerfile.labtainer.master.headless
cp -aR workspace/system workspace_master/
cp -a $LABTAINER_DIR/headless-lite/motd workspace_master
cp -a $LABTAINER_DIR/headless-lite/docker-entrypoint workspace_master
cp -a  $LABTAINER_DIR/headless-lite/wait-for-it.sh workspace_master
cp -a  $LABTAINER_DIR/headless-lite/doterm.sh workspace_master
cp -a  $LABTAINER_DIR/headless-lite/doupdate.sh workspace_master
cd workspace_master

cat <<EOT >bashrc.labtainer.master
   if [[ ":\$PATH:" != *":./bin:"* ]]; then 
       export PATH="\${PATH}:./bin:/home/labtainer/labtainer/trunk/scripts/designer/bin:/home/labtainer/labtainer/trunk/testsets/bin"
       export LABTAINER_DIR=/home/labtainer/labtainer/trunk
   fi
EOT

CACHE="--no-cache"
LABTAINER_DEV="FALSE"
while [[ -n "$1" ]]; do
    if [[ "$1" == -h ]]; then
        echo "use -c to build with cache"
        echo "use -d to build developer version, otherwise pulls from distribution"
        exit 0
    fi
    if [[ "$1" == -c ]]; then
        CACHE=""
        shift
    fi
    if [[ "$1" == -d ]]; then
        LABTAINER_DEV="TRUE"
        shift
    fi
done
if [[ "$LABTAINER_DEV" != "TRUE" ]]; then
    echo "Getting labtainer.tar from NPS distribution."
    wget https://nps.box.com/shared/static/afz87ok8ezr0vtyo2qtlqbfmc28zk08j.tar -O labtainer.tar
else
    echo "Getting labtainer.tar from your distrib, assuming mkdist.sh was run."
    cp -a $LABTAINER_DIR/distrib/labtainer.tar ./
fi     
docker build $CACHE --build-arg DOCKER_GROUP_ID="$(getent group docker | cut -d: -f3)" -f Dockerfile.labtainer.master.headless -t labtainer.master.headless:latest .
docker tag labtainer.master.headless labtainers/labtainer.master.headless
cd $here
