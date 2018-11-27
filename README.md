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
