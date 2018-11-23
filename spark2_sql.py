from pyspark.sql import Sparksession
from pyspark.sql import Row
from pyspark.sql import functions

def loadMovieNmaes():
	movieNames = {}
	with open('ml-100k/u.items') as f:
		for line in f:
			fields = line.split('|')
			movieNames[int(fileds[0])] = fileds[1]

	return movieNames

def parseInput(line):
	fields = line.split()
	# create Row object
	return Row(moiveID = int(fields[1]), rating = float(fields[2]))

if __name__ == '__main__':
	# create sparksession
	spark = SparkSession.builder.appName('PopularMovies').getOrCreate()

	#Load up  our movie ID -> name dictionary
	movieNames = loadMovieNames()

	# Get the raw data (RDD)
	lines = spark.sparkContext.textFile("hdfs:///user/maria_dev/ml-100k/u.data")

	# convert it to a RDD of Row objects with (movieID, rating)
	movies = line.map(parseInput)
    
	# then convert it to DataFrame since now we have Row 
	# by convention let's call it dataset
	movieDataset = spark.createDataFrame

	# then you can easily compute the average
	averageRating = movieDatset.groupBy("movieID").avg("rating")

	# and the count
	counts = movieDataset.groupBy("movieID").count()

	# join the two together so we will have movie ID, avg ratings, and count columns
	averagesAndCounts = counts.join(averageRatings, "movieiD")

	# pull the top 10
	topTen = averagesAndCounts.orderBy("avg(rating)").take(10)

	# print them out, converting movie ID's to names as we go
	for movie in topTen:
		print(movieNames[movie[0]], movie[1], movie[2])

    # stop the session
    spark.stop()


