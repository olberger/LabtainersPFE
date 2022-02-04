#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
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
# Install Docker on an Arch system, along with other packages required by Labtainers
#

#Check if current user is user login. (Targeted to avoid adding root user into docker group instead of the the user logged in account.)
currUser=`who | awk '{print $1}'`
if [ "$USER" != "$currUser" ]; then
    echo "You are not the login user. If you are root user, please exit. And run this script again."
    exit
fi

type sudo >/dev/null 2>&1 || { echo >&2 "Please install sudo.  Aborting."; exit 1; }
sudo -v || { echo >&2 "Please make sure user is sudoer.  Aborting."; exit 1; }
#---needed packages for install
version=$(lsb_release -a | grep Release: | cut -f 2)
docker_package=docker

#---initial check for packages already installed otherwise install them
#---installs python modules directly through Arch official repos
#---prevents environment conflicts given the Arch rolling release model
declare -a packagelist=("ca-certificates" "curl" "device-mapper" "$docker_package" "python-pip" "python-dateutil" "python-parse" "python-netaddr" "gnupg" "lvm2" "openssh" "xterm")
for i in "${packagelist[@]}"
do
packagecheck=$(pacman -Q $i 2> /dev/null)
    if [ -z "$packagecheck" ]; then
        sudo pacman -Su $i
        RESULT=$?
        if [ $RESULT -ne 0 ];then
            echo "problem fetching '$i' package, exit"
            exit 1
        fi
        else
            echo "package '$i' already installed"
    fi
done

#---starts and enables docker
sudo systemctl start docker
sudo systemctl enable docker

#---gives user docker commands
sudo groupadd docker || true
sudo usermod -aG docker $USER || true 

#---Checking if packages have been installed. If not, the system will not reboot and allow the user to investigate.
packagefail="false"
for i in "${packagelist[@]}"
do
#echo $i
packagecheck=$(pacman -Q $i 2> /dev/null)
#echo $packagecheck
    if [ -z "$packagecheck" ]; then
       if [ $i = $docker_package ];then 
           echo "ERROR: '$i' package did not install properly. Please check the terminal output above for any errors related to the pacakge installation. If the issue persists, go to docker docs and follow the instructions for installing docker. (Make sure the instructions is for your Linux distribution,e.g., Ubuntu and Fedora.)"
       else
           echo "ERROR: '$i' package did not install properly. Please check the terminal output above for any errors related to the pacakge installation. Try installing the '$i' package individually by executing this in the command line: 'pacman -Su $i" 
       fi 
       packagefail="true"
       #echo $packagefail
    fi
done

declare -a piplist=("dateutil" "parse" "netaddr")
for i in "${piplist[@]}"
do
pipcheck=$(pip list 2> /dev/null | grep -F $i)
    if [ -z "$pipcheck" ]; then
        echo "ERROR: '$i' package did not install properly. Please check the terminal output for any errors related to the pacakge installation. Make sure 'python-pip' is installed and then try running this command: 'sudo pacman -Su python-$i' "
        packagefail="true"
    fi
done

if [ $packagefail = "true" ]; then
    echo "If you manually install packages to correct the problem, be sure to reboot the system before trying to use Labtainers."
    exit 1
fi

exit 0

#Notes: The �-y� after each install means that the user doesn�t need to press �y� in between each package download. The install script is based on this page: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
