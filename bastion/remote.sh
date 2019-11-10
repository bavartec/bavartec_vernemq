set -e

mkdir -p /tmp/"$1"/
sshfs "$2":/home/ubuntu/ /tmp/"$1"/

cp -r -L "$1" /tmp/"$1"/

fusermount -uz /tmp/"$1"/
rmdir /tmp/"$1"

ssh -t "$2"
ssh -t "$2"
