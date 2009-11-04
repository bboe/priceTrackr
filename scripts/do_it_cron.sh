#!/bin/sh

if [ $# -ne 1 ]
then
    echo "Usage: $0 csil_name"
    exit 1
fi

echo "Starting: `date`"

host1=bboe@$1.cs.ucsb.edu
temp_path=seclab/cron_temp
archive_path=/home/bryce/src/priceTrackr/ARCHIVE/
pt_path=src/priceTrackr/scripts
key=/home/bryce/.ssh/ptrackr.priv

# Perform crawl
ssh $host1 -i $key "mkdir $temp_path && cd $temp_path && ../priceTrackr/newegg_crawler.py --limit 1"
if [ $? -ne 0 ]
then
    echo "Crawl failed"
    exit 1
fi

# Copy data to archive folder
scp -i $key $host1:$temp_path/* $archive_path
if [ $? -ne 0 ]
then
    echo "SCP data to local failed"
    exit 1
fi

# Copy pkl file to webserver
filename=`ls -tr $archive_path/*.pkl | tail -n 1`
scp -i $key $filename pricetrackr:src/priceTrackr/scripts
if [ $? -ne 0 ]
then
    echo "SCP data to remote failed"
    exit 1
fi

# Remove files on host1
ssh $host1 -i $key "rm -rf $temp_path"
if [ $? -ne 0 ]
then
    echo "Could not delete files"
    exit 1
fi

# Insert data into database
ssh pricetrackr -i $key "cd $pt_path && ./process_data.py *.pkl"
if [ $? -ne 0 ]
then
    echo "Could not import data"
    exit 1
fi

# Remove file on webserver
ssh pricetrackr -i $key "rm $pt_path/*.pkl"
if [ $? -ne 0 ]
then
    echo "Could not delete pkl file"
    exit 1
fi

echo "Finished: `date`"
echo