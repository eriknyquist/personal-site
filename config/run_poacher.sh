#!/bin/bash

CONFIG=/home/ubuntu/site-poacher-config.json
POACHER=/home/ubuntu/yourlifecalendar/GithubPoacher

cd $POACHER
python2.7 poacher.py -f $CONFIG
