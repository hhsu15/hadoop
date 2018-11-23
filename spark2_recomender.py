from pyspark.sql import SparkSession
from pyspakr.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.sql.functions import lit

def loadMovieNames():
	movieNames = {}
	with open('ml-100k/u.ite') as f:
		for line in f:
		fields = line.split('|')
		movieNames[int(fields[0])] = fields[1].decode('ascii', 'ignore')
	return movieNames

def parseInput(line):
	fields = line.value.split()
	return Row(userID = int(fields[0]), movieID = int(fields[1]), rating = float(fields[2]))

if __name__ == '__main__':
	spark = SparkSession.builder.appName("MovieRecs").getOrCreate()

	movieNames = loadMovieNames()

	# get raw data
	lines = spark.read.text("hdfs:///user/maria_dev/ml-100k/u.data").rdd

	# convert it to a RDD of Row objects with (userID, movieID, rating)
	ratingsRDD = lines.map(parseInput)

	# convert it to a dataframe and cache it
	ratings = spark.createDataFrame(ratingsRDD).cache()

	# create an ALS collaborative filtering model from the complete data set
	als = ALS(maxIter=5, regParam=0.01, userCol='userID', itemCol='movieID',ratingCol='rating')
	model = als.fit(ratings)

	# print out ratings from user 0
	print('\nRatings for user ID0:')
	userRatings = ratings.filter('userID=0')
	for raitng in userRatings.collect():
		print(movieNames[rating['movieID']], rating['rating'])
	
	print('\nTop 20 recommendations:')

	# find movies rated more than 100 times
	ratingCount = ratings.rougpBy('movieID').count().filter('count > 100')

	# contruct a test datafrome for user 0 with every movie rated more than 100 times
	popularMovies = ratingCounts.select('movieID').withColumn('userID', lit(0))
	recommendations = model.transform(popularMovies)

	topRecommendations = recommendations.sort(recommendations.prediction.desc()).take(20)

	for recommendation in topRecommendations:
		print(movieNames[recommendation['movieID']], recommendation['prediction'])
		spark.stop()

