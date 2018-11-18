- # hadoop
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
