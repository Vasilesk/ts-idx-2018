#! /bin/sh
nohup ./make_dict.py > /dev/null 2> /dev/null < /dev/null &
while [ ! -f trigger ]
do
  sleep 2
done
sleep 1
rm trigger
