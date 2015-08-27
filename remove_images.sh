#!/bin/bash

for f in $(find DFD/static/images/ -name "*.png"); do
    timestamp=$(stat $f | grep Access | grep -v Uid | cut -d" " -f2,3 | tr -d "-" | tr -d " " | tr -d ":" | cut -d "." -f1)
    diff=$(( `date '+%Y%m%d%H%M%S'` - $timestamp ))
    if [ $diff -gt 86400 ]
    then
        rm $f
        echo "Removing file $f"
    fi
done

