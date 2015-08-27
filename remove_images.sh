#!/bin/bash

for f in $(find DFD/static/images/ -regex ".*\.\(png\|gif\)" -atime 1); do
    rm $f
    echo "Removing file $f"
done

