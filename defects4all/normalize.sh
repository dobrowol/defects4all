#!/bin/bash
columns=4
if [ "$#" -eq 0 ]; then
	echo "usage normalized.sh <dir_name> [optional]<runtime>"
fi
if [ "$#" -eq 2 ]; then
	
	columns=6
fi
directory=$1
mkdir -p "$directory"/normalized
cp "$directory"/*log "$directory"/normalized/
for filename in "$directory"/normalized/*log; do
	echo "normalizing $filename"
	cut -d ' ' -f $columns- $filename > tmp.file
	mv tmp.file $filename
done

