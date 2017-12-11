#!/bin/bash -x

#Below will not work on windows.
BASEDIR=`pwd`
sudo apt-get update >> /tmp/reanTest.install.log 2>&1

sudo mkdir -p /var/reanTest
#sudo mkdir -p /var/reanTest/conf
cd $BASEDIR
#Will only work on Ubuntu for now.
sudo apt-get install python-pip python-dev build-essential -y >> /tmp/reanTest.install.log 2>&1
sudo pip install --upgrade pip  >> /tmp/reanTest.install.log 2>&1
sudo pip install --upgrade virtualenv >> /tmp/reanTest.install.log 2>&1
sudo pip install reantest-0.1-py3-none-any.whl --upgrade >> /tmp/reanTest.install.log 2>&1

echo "ReanTest installed successfully!!!"
