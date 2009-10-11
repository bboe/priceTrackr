#!/bin/sh

start=`date +%s`

./makeList.php $* | ./processList.py $* | ./finishList.php $*
finish=`date +%s`

echo 'Completion Time:' `expr $finish - $start`s
