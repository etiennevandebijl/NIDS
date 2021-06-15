#!/bin/bash

#INPUT
PROJECT="Intrusion-Detection-Datasets"
DATASET="CIC-IDS-2018"
FOLDERNAME="Captures"

#OUTPUT
ZEEK="Zeek-4.0.0"

#USEFULL VARIABLE
CURRENT="$PWD"

PCAP_PATHS=$(find $PWD/"$PROJECT"/$DATASET/$FOLDERNAME/ -type f)
for i in $PCAP_PATHS
do
	echo ${i/"$PWD"/}

# 	pcapfix -d -o "$i" "$i"
	
	NEW_FOLDER=${i/"$FOLDERNAME"/"$ZEEK"}
	if [[ $NEW_FOLDER == *".pcap"* ]]; then
	 	NEW_FOLDER=${NEW_FOLDER/".pcap"/"/"}
	fi

	mkdir -p $NEW_FOLDER
	cd $NEW_FOLDER
	zeek -C -H seed.txt -r $i "$CURRENT"/log-reduction.zeek
	cd "$CURRENT"
done