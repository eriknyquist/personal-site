#!/bin/bash

CONFIG=/home/ubuntu/site-poacher-config.json
POACHER=/home/ubuntu/GithubPoacher

while [ ! -p /home/ubuntu/poacherfifo ]
do
	sleep 1
done

cd $POACHER
python2.7 poacher.py -f $CONFIG
