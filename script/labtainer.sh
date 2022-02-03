#install docker
sudo apt -y install apt-transport-https ca-certificates curl software-properties-common
sudo apt-get install -y docker.io
sudo groupadd docker
sudo usermod -aG docker $USER
sudo usermod -aG docker $(users)
#install curl
sudo apt install -y curl

cd $HOME
wget https://codeload.github.com/IlyesBenighil/LabtainersPFE/zip/refs/heads/master
unzip master
mv LabtainersPFE-master labtainer
sudo chmod -R 777 labtainer
cd labtainer
./install-labtainer.sh
