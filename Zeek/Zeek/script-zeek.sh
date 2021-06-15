#!/bin/bash

#INPUT
PROJECT="Intrusion-Detection-Datasets" #Folder where all pcaps are stored + log files when extracted (See Zeek/Zeek/readme.md)
DATASET="CIC-IDS-2018" #Dataset to convert
FOLDERNAME="Captures"

#OUTPUT
ZEEK="Zeek-4.0.0" #This is the folder where all outputs will be stored (and thus the corresponding version)

#USEFULL VARIABLE
CURRENT="$PWD"

PCAP_PATHS=$(find $PWD/"$PROJECT"/$DATASET/$FOLDERNAME/ -type f)
for i in $PCAP_PATHS
do
	echo ${i/"$PWD"/} #Print for verbose

# 	pcapfix -d -o "$i" "$i" #this can fix broken packets in pcap. Can be turned on if required (I did that)
	
	NEW_FOLDER=${i/"$FOLDERNAME"/"$ZEEK"}
#	
	if [[ $NEW_FOLDER == *".pcap"* ]]; then
	 	NEW_FOLDER=${NEW_FOLDER/".pcap"/"/"}
	fi

	mkdir -p $NEW_FOLDER
	cd $NEW_FOLDER
	zeek -C -H seed.txt -r $i "$CURRENT"/disable_streams.zeek #Perform Zeek
	cd "$CURRENT"
done
