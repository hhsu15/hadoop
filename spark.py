# Introducing RDD (Resilient Distributed Dataset)
# An abstraction
# RDD is created by your driver program and made RDD reilent and distribute
# The Spark shell creates a `sc` (spark context) object for you
# spark is almost able to transform any datatype into RDD

from pyspark import SparkConf, SparkContext

def loadMovieNames():
	movieNames = {}
	with open("ml-100k/u.item") as f:
		for line in f:
		fields = line.split('|')
		movieNames[int(fields[0])] = fields[1]
		return movieNames


def parseInput(line):
	fields = line.split()
	return (int(fields[1]), float(fields[2]), 1.0))

if __name__ == "__main__":
	# create configuration
	conf = SparkConf().setAppName("WorstMovies")
	# create spark context
	sc = SparkContext(conf=conf)

	movieNames = loadMovieNames()
    # load the raw data and create RDD object
	lines = sc.textFiel("hdfs:///user/maria_dev/ml-100k/u.data")
    
	# this will convert it to (movieID, (rating, 1.0))
	movieRatings = lines.map(parseInput)
	
	# reduce to (movieID, (sumOfRatings, totalRatings))
	ratingTotalsAndCount = movieRatings.reduceByKey(lambda movie1, movie2: (movie1[0] + movie2[0]))

	# Map to (movieID, averageRating)
	averageRatings = ratingTotalsAndCount.mapValues(lambda totalAndCount: totalAndCount[0] /totalAndCount[1]

	# Sort by average rating
	soredMovies = averageRatings.sortBy(lambda x: x[1])

	# Take the top 10 results
	results = sortedMovies.take(10)

	for result in results:
		print(movieNames[result[0]], result[1])
