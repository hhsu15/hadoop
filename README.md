# hadoop
## Getting set up
- Install VirtualBox 
- Hortonworks sandbox (15GB! - be careful this is super big) - install version 2.5 otherwise it's going to blow up
- make sure you change the ram to what you can afford, eg 3GB rather than 8 GB

### Ambari UI
- Once you are in you can go to the browser with localhost:8888 and see the Ambari UI
- The UI should be pretty straight forward. You can use Hive view to run some SQL query

### Commend Line Interface
- Create your local env
  - on terminal, run
  ```
  ssh maria_dev@127.0.0.1 -p 2222
  ```
  - Enter password: `maria_dev`

- Hadoop commends
  - see hadoop filesystem
  ```
  hadoop fs -ls
  ```

  - make folder
  ```
  hadoop fs -mkdir myFolder
  ```
  
  - get a file from web
  ```
  wget http://media.sundog-soft.com/hadoop/m1-1ook/u.data
  ```

  - copy your local file to hdfs
  ```
  hadoop fs -copyFromLocal u.data myFolder
  ```
## Create Admin login 
- login as super user
```
su root 
```
- after enter your password

```
ambari-admin-password-password-reset
```

### Get the env set up again..
- Will have to start with installing pip, vim, and then mrJob packages
- Just follow through the video. There is quite a lot gocha

### Run mapreduce srcipt
- Run on local
```
python RatingBreakdown.py u.data
```

- Run on hadoop cluster
```
python RatingsBreakdown.py -r hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar u.data
```

## MySQL
- Login as root and enter password "hadoop"
```
mysql -u root -p
```
- create database
```
mysql> create database movielens;
```
- show databases
```
mysql> show databases;
```
- getting set up
```
mysql> SET NAMES 'utf8';
mysql> SET CHARACTER SET utf8;
```

- now use the database we just created
```
mysql>use movielens
```
- run the sql file
```
mysql>source movielen.sql
```
- now the query is executed, let's take a look
```
mysql>show tables
```
- and the actual data
```
mysql>select * from movies limit 10;
```
- to see the schema
```
mysql> describe ratings
```

- Privilege table, so we can run sqoop
```
mysql> GRANT ALL PRIVILEGES ON movielens.* to ''@'localhost';
mysql> exit
```

- connecting through jdbc to mysql database on localhost to the movielens dabtanase. `-m 1` means we are using only 1 mapper (because we have a small dataset)
```
sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1
```
- Then go to the Ambari UI and you will see a folder named movies created under usr home directory. Congrast! Now we have got our data from mysql database into the hadoop cluster using sqoop!

- If all you want to do is to put into Hive..not create a folder in HDFS then..
```
sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1 --hive-import
```
- Again you can go to Ambari UI and check into the Hive view to confirm if the table is created and you can run query aginst it.
- With Hortonworks, the data for Hive resides in apps->hive->warehouse (this is where you can find the movies folder
- You can also import data from hdfs back to mysql. Need to create the table ahead of time since sqoop is not going to create the table for you.
```
mysql> use movielens;
mysql> CREATE TABLE exported_movies (id INTEGER, title VARCHAR(255), releaseDate DATE);
mysql> exit
```
- Then use sqoop command:
```
sqoop export --connect jdbc:mysql://localhost/movielens -m 1 driver com.mysql.jdbc.Driver --table expoerted_movies --export-dir /apps/hive/warehouse/movies --input-fields-terminated-by '\0001
```

## NoSQL
### HBase Set up
- Set up the port so python can talk to the rest service on top of the HBase
- On the VirtualBox, settings -> NetWork -> advance -> Port Forwarding
- Click on the plus sign and add a new record like
- HBase REST, TCP, 127.0.0.1, 8000, , 8000
- Login to Ambrari, -> Services -> HBase -> Service Actions -> Start
- Now HBase is running
#### Launch a REST server 
- Rest server sitting on top of HBase so we can communicate with the outside world.
- Login as root by using
```
su toot
```
And then enter the following to start server:
```
/usr/hdp/current/hbase-master/bin/hbase-daemon.sh start rest -p 8000 --infoport 8001
```
- to stop
```
/usr/hdp/current/hbase-master/bin/hbase-daemon.sh stop rest
```


