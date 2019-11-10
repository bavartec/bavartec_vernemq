set -e

mkdir -p /tmp/bastion/
sshfs "$1":/home/ubuntu/ /tmp/bastion/

cp -r -L api db mqtt bastion/* /tmp/bastion/
cp -r -L .ssh/* /tmp/bastion/.ssh/

fusermount -uz /tmp/bastion/
rmdir /tmp/bastion/

ssh -t "$1"
