#!/bin/sh

echo "Starting: `date`"

key=~/.ssh/ptrackr.priv
local_archive_path=~/hg/priceTrackr/ARCHIVE

crawler=bboe@192.35.222.100
crawler_temp_path=cron_temp
crawler_script_path=~/hg/priceTrackr/scripts

server=bboe@128.111.48.223
server_script_path=~/hg/priceTrackr/scripts

# Perform crawl
ssh crawler -i $key "rm -rf $crawler_temp_path && mkdir $crawler_temp_path && cd $crawler_temp_path && $crawler_script_path/newegg_crawler.py --threads 4"
if [ $? -ne 0 ]
then
    echo "Crawl failed"
    exit 1
fi

# Copy data to archive folder
scp -i $key $crawler:$crawler_temp_path/* $local_archive_path/
if [ $? -ne 0 ]
then
    echo "SCP data to local failed"
    exit 1
fi

# Copy pkl file to webserver
filename=`ls -tr $local_archive_path/*.pkl | tail -n 1`
scp -i $key $filename $server:$server_script_path
if [ $? -ne 0 ]
then
    echo "SCP data to remote failed"
    exit 1
fi

# Remove files on host1
ssh $crawler -i $key "rm -rf $temp_path"
if [ $? -ne 0 ]
then
    echo "Could not delete files"
    exit 1
fi

# Insert data into database
ssh $server -i $key "cd $server_script_path && ./process_data.py *.pkl"
if [ $? -ne 0 ]
then
    echo "Could not import data"
    exit 1
fi

# Remove file on webserver
ssh $server -i $key "rm $server_script_path/*.pkl"
if [ $? -ne 0 ]
then
    echo "Could not delete pkl file"
    exit 1
fi

# Generate pages on webserver
ssh $server -i $key "$server_script_path/generate_pages.py"
if [ $? -ne 0 ]
then
    echo "Could not generate pages"
    exit 1
fi


echo "Finished: `date`"
echo