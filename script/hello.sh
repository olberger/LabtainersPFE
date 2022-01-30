#!/bin/bash -eu

echo "HELLO FROM SCRIPT"
pwd
#apt -y install --no-install-recommends tasksel
export DEBIAN_FRONTEND="noninteractive"
echo $DEBIAN_FRONTEND
sudo apt install -y ubuntu-desktop
#sudo tasksel install kubuntu-desktop
