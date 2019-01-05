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
#### Pig and HBase working together
- Log into the HBase shell
```
hbse shell
```
- Create a table 
```
hbase(main):001:0> create 'users', 'userinfo'
```
- refer to `/pig/hbase.pig`

### Cassandra
Another NoSQL database whcih provides CQL query language to be able to do SQL like queries. Focus more on availability than consistency (--eventually consistent)
- Set up (TODO)
- Refer to `CassandraSpark.py` 
```
spark-submit --package datastax:spark-cassandra-connector:2.0.0-M2-s 2.11 CassandraSpark.py
```
### MongoDB
Singble master node. Consisteny over availability

Get get up for MongoDB
- go to the service directory
```
[root@sandbox maria_dev]# cd /var/lib/ambari-server/resources/stacks//HDP/2.5/services
```
- clone from git
```
[root@sandbox services]# git clone https://github.com/nikunjness/mongo-ambari.git
```
- restart the service
```
[root@sandbox services]# sudo service ambari restart
```
- then log into Ambari as admin
- click on Action -> Add Service -> check Mongo DB
- once Mongo DB is installed, you need to install python package
```
pip install pymongo
```
- to run the script, specify the connector version from mongodb:
```
export SPARK_MAJOR_VERSION=2
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.0.0 mongodb.py
```
#### mongodb command line
```
[maria_dev@sandbox ~]$ mongo
```
```
> use movielens
```
- the scrips are similar to javascript, to find record by user_id
```
> db.users.find( {user_id: 100} )
```
- to see exactly what's happening you can use explain
```
db.users.explain().find( {user_id:100})
```
- since mongodb does not index by default, to make it efficient, we can create the index by running:
```
db.users.createIndex( {user_id: 1}) 
```
- aggregate by occupation and show average age for each occupation
```
> db.users.aggregate([
... { $group: { _id: {occupation: "$occupation"}, avgAge: { $avg: "$age" }}}
... ])
```
- count of records
```
> db.users.count()
```
- Finally, make sure you shut down MongoDB service correctly otherwise it may crash everything!!

## Apache Drill
Makes everthing SQL
- Example: make query between Hive and MongoDB
- Start MongoDB and import data into it
- Go to Hive and create a database by running 
```
CREATE DATABASE movielens;
```
- Then load data into it (like we did and make sure you select movielens as database)

- Then load the data into MongoDB (make sure you have the file in your HDSF)
```
export SPARK_MAJOR_VERSION=2
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.0.0 MongoSpark.py
```
- Download Drill
```
[root@sandbox maria_dev]# wget http://archive.apache.org/dist/drill/drill-1.12.0/apache-drill-1.12.0.tar.gz
```
- Decompress the file
```
tar -xvf apache-drill-1.12.0.tar.gz
- Run drill. cd into the folder 
[root@sandbox apache-drill-1.12.0]# bin/drillbit.sh start -Ddrill.exec.port=8765
```
- TODO (somehow failed to start the web on local..)

## Phoneix
- Originally developed by SalesForce then open sourced
- works with HBase
- TODO

## Presto
- Built by Facebook
- works well with Cossandra and others

## Cluster management
- Yarn - Resouce negotiator
- Tez - faster than MapReduce
- Mesos (like Yarn but works more in genereal not just for Hadoop)
- ZooKeeper
  - Command line interface
```
[root@sandbox ~]# cd /usr/hdp/current/zookeeper-client/bin
[root@sandbox bin]# ./zkCli.sh # connect to zookeeper
```
- once you are in zookeeper, it looks like a filesystem
- you can run `ls /` to see what's in currect directory
- let's mess around with it. create a znode(master node) and store string to it. call it testmaster
```
[zk: localhost:2181(CONNECTED) 2] create -e /testmaster "127.0.0.1:1234" 
[zk: localhost:2181(CONNECTED) 4] get /testmaster # get the info about the testmaster
[zk: localhost:2181(CONNECTED) 4] quit  # to zookeeper this is like the node just died
[root@sandbox bin]# ./zkCli.sh # connect to zookeeper # log back to zookeeper
[zk: localhost:2181(CONNECTED) 4] get /testmaster # get the info about the te
stmaster # this will say the node does not exist
# so this is the case I will nominate myself as the znode
[zk: localhost:2181(CONNECTED) 2] create -e /testmaster "127.0.0.1:1234"
# you won't be able to create one if already exists
```
## OOZIE
- task scheduler in Hadoop
- you can chain things and create a workflow (like run Pig, Hive and then MongoDB...)
- written(like configuration) through XML

## Zeppelin
- A tool to do your data science work in a cluster easily
- Notebook interface - use 127.0.0.1:9995
- create a notebook and click on the settings(gear icon) and make sure spark is at the top

## Kafka
- Messaging system
- Topic based (data published to a topic and you have client listening to the topic)

- let's create a topic
```
[maria_dev@sandbox ~]$ cd /usr/hdp/current/kafka-broker/
# create topic called fred
[maria_dev@sandbox bin]$ ./kafka-topics.sh --create --zookeeper sandbox.hortonworks.com:2181 --replication-factor 1 --partitions 1 --topic fred

# show all the topics
[maria_dev@sandbox bin]$ ./kafka-topics.sh --list --zookeeper sandbox.hortonworks.com:2181
```
- kick off kafka producer will be wating for consumer
```
[maria_dev@sandbox bin]$ ./kafka-console-producer.sh --broker-list sandbox.hotonworks.com:6667 --topic fred

this is a line of data
I am sending this on the fred topic
```

- create a consumer(kafka receiver) using another terminal
```
[maria_dev@sandbox bin]$ ./kafka-console-consumer.sh --bootstrap-server sandbox.hortonworks.com:6667 --zookeeper localhost:2181 --topic fred--from-beginning
```

## Flume
- Simliar to Kafka
- Desinged to aggreate logs, acting as a buffer between log source and the database, say HBase
- built in hortonworks
- configuration driven - setting up source, sink and channel
- refer to the configuration file
- On the separate terminal run the following to kick off the listener
```
[maria_dev@sandbox ~]$ cd /usr/hdp/current/flume-server/
[maria_dev@sandbox flume-server]$ bin/flume-ng agent --conf conf --conf-file ~/example.conf --name a1 -Dflume.root.logger=INFO,console
```
- Then another terminal, run
```
[maria_dev@sandbox ~]$ telnet localhost 44444
# then you can start typing something to test
```

## Streaming Data Processing
### Spark Streaming
Use Spark Streming with Flume to process streaming data
```
[maria_dev@sandbox ~]mkdir checkpoint # create a checkpoint directory
[maria_dev@sandbox ~]export SPARK_MAJOR_VERSION=2
# kick off spark code
[maria_dev@sandbox ~]spark-submit --packages org.apache.spark:spark-streaming-flume_2.11:2.0.0 SparkFlume.py
```
- Kick off Flume in another machine
```
[maria_dev@sandbox ~]$ cd /usr/hdp/current/flume-server/
[maria_dev@sandbox flume-server]$ bin/flume-ng agent --conf conf --conf-file ~/sparkstreamingflume.conf --name a1
```
### Storm
- Truely realtime (as opposed to batch interval like Spark Streaming)
- Use Java, hardly any other languages
- Preinstalled in hortonworks
- Works well with Kafka

## Flink
- Another streaming processing engine, similar to Storm, true realtime
- youngest in these technologies

