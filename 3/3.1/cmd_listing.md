# Практика HDFS

Листинг команд:

```
[cloudera@quickstart ~]$ cd /media/share/DE
[cloudera@quickstart DE]$ ls
voyna-i-mir-tom-1.txt  voyna-i-mir-tom-2.txt  voyna-i-mir-tom-3.txt  voyna-i-mir-tom-4.txt
[cloudera@quickstart DE]$ hadoop fs -put voyna-i-mir-tom-* /DE/3.1/
put: `/DE/3.1/': No such file or directory
[cloudera@quickstart DE]$ hadoop fs -mkdir -p /DE/3.1/
[cloudera@quickstart DE]$ hadoop fs -put voyna-i-mir-tom-* /DE/3.1/
[cloudera@quickstart DE]$ hadoop fs -ls /DE/3.1/
Found 4 items
-rw-r--r--   1 cloudera supergroup     736519 2022-11-09 22:33 /DE/3.1/voyna-i-mir-tom-1.txt
-rw-r--r--   1 cloudera supergroup     770324 2022-11-09 22:33 /DE/3.1/voyna-i-mir-tom-2.txt
-rw-r--r--   1 cloudera supergroup     843205 2022-11-09 22:33 /DE/3.1/voyna-i-mir-tom-3.txt
-rw-r--r--   1 cloudera supergroup     697960 2022-11-09 22:33 /DE/3.1/voyna-i-mir-tom-4.txt
[cloudera@quickstart DE]$ hadoop fs -cat /DE/3.1/* | hadoop fs -appendToFile - /DE/3.1/voyna-i-mir.txt
[cloudera@quickstart DE]$ hadoop fs -ls /DE/3.1/
Found 5 items
-rw-r--r--   1 cloudera supergroup     736519 2022-11-09 22:33 /DE/3.1/voyna-i-mir-tom-1.txt
-rw-r--r--   1 cloudera supergroup     770324 2022-11-09 22:33 /DE/3.1/voyna-i-mir-tom-2.txt
-rw-r--r--   1 cloudera supergroup     843205 2022-11-09 22:33 /DE/3.1/voyna-i-mir-tom-3.txt
-rw-r--r--   1 cloudera supergroup     697960 2022-11-09 22:33 /DE/3.1/voyna-i-mir-tom-4.txt
-rw-r--r--   1 cloudera supergroup    3048008 2022-11-09 22:39 /DE/3.1/voyna-i-mir.txt
[cloudera@quickstart DE]$ hadoop fs -rm /DE/3.1/voyna-i-mir-tom-*
Deleted /DE/3.1/voyna-i-mir-tom-1.txt
Deleted /DE/3.1/voyna-i-mir-tom-2.txt
Deleted /DE/3.1/voyna-i-mir-tom-3.txt
Deleted /DE/3.1/voyna-i-mir-tom-4.txt
[cloudera@quickstart DE]$ hadoop fs -ls /DE/3.1/
Found 1 items
-rw-r--r--   1 cloudera supergroup    3048008 2022-11-09 22:39 /DE/3.1/voyna-i-mir.txt
[cloudera@quickstart DE]$ hadoop fs -chmod 755 /DE/3.1/*
[cloudera@quickstart DE]$ hadoop fs -ls /DE/3.1/
Found 1 items
-rwxr-xr-x   1 cloudera supergroup    3048008 2022-11-09 22:39 /DE/3.1/voyna-i-mir.txt
[cloudera@quickstart DE]$ hadoop fs -du /DE/3.1/
3048008  3048008  /DE/3.1/voyna-i-mir.txt
[cloudera@quickstart DE]$ hadoop fs -du -s /DE/3.1/
3048008  3048008  /DE/3.1
[cloudera@quickstart DE]$ hadoop fs -du -h /DE/3.1/
2.9 M  2.9 M  /DE/3.1/voyna-i-mir.txt
[cloudera@quickstart DE]$ hadoop fs -setrep -w 2 /DE/3.1/
Replication 2 set: /DE/3.1/voyna-i-mir.txt
Waiting for /DE/3.1/voyna-i-mir.txt .........................................^C[cloudera@quickstart DE]$ hadoop fs -setrep -wdu -h
2.9 M  5.8 M  /DE/3.1/voyna-i-mir.txt
[cloudera@quickstart DE]$ hadoop fs -cat /DE/3.1/voyna-i-mir.txt | wc -l
10272

```