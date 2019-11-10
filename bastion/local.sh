set -e

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install sshfs nmap

echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf > /dev/null
sudo iptables -t nat -A POSTROUTING -o eth0 -s 20.0.0.0/16 -j MASQUERADE
