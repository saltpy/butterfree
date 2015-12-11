#!/usr/bin/env bash

. $1/env/bin/activate

$1/butterfree.py issue tact >> $1/butterfree.csv
