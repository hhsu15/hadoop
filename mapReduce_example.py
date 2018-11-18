'''MapReducer job example using MRJob lib'''

from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingBreakdown(MRJob):
	def steps(self):
	"""tells what mapper and reducer we have"""
		return [
			MRStep(mapper=self.mapper_get_ratings,
				   reducer=self.reducer_count_ratings)
		]

	def mapper_get_rattings(self, _, line):
	"""mapper """
		(userID, movieID, rating, timestamp) = line.split('\t')
		yield rating, 1

	def reducer_count_rating(self, key, values):
	"""reducer"""
		yield key, sum(values)


if __name__ == '__main__':
		RatingBreakdown.run()

