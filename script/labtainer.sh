#install docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt -y update
sudo apt install -y docker-ce


cd $HOME
wget https://codeload.github.com/IlyesBenighil/LabtainersPFE/zip/refs/heads/master
unzip master
mv LabtainersPFE-master labtainer
chmod 777 labtainer
cd labtainer
./install-labtainer.sh