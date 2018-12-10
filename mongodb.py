from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

def parseInput(line):
	fields = line.split('|')
	return Row(user_id=int(fields[0], age=int(fields[1]), gender=fields[2], occupation=fields[3], zip=fields[4])

if __name__ == '__main__':
	# create sparksession
	spark = SparkSession.builder.appName("MongoDBIntegration").getOrCreate()

	# get raw data
	lines = spark.sparkContext.textFile("hdfs://user/maria_dev/ml-100k/u.user")

	# convert it to a RDD with (userid, age, gender, occupation, zip)
	users = lines.map(parseInput)

	# convert that to a DataFrame
	userDataset = spark.createDataFrame(users)

	# write it to MongoDB
	userDataset.write\
		.format("com.mongodb.spark.sql.DefaultSource")
		.option("url", "mongodb://127.0.0.1/movielens.users")\
		.mode('append')\
		.save()
   
   # read it back from mongoDB into a new DataFrame
    readUsers = spark.read\
       .format("com.mongodb.spark.sql.DefaultSource")\
	   .option("url", "mongodb://127.0.0.1/movielens.users")\
	   .load()
	
	readUsers.createOrReplaceTempView("users")

	sqlDF = spark.sql("SELECT * FROM users WHERE age < 20")
	sqlDF.show()

	# stop session
	spark.stop()
   
