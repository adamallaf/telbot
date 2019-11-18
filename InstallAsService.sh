#!/bin/sh

echo -n " * Installing telbot as service..."
# TODO install as python package
BOTDIR=`pwd`
TELBOTSERVICE=telbot.service
sed 's-BOTDIR-'$BOTDIR'-g' serviceTemplate > $TELBOTSERVICE

cp $TELBOTSERVICE /etc/systemd/system
systemctl enable $TELBOTSERVICE
systemctl start $TELBOTSERVICE
echo " ** done **"
