set -e

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io

sudo iptables -A INPUT -i docker0 -j ACCEPT

sudo service docker start
sudo usermod -a -G docker ubuntu

yes '' | sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get -y install certbot python3-certbot-dns-route53
