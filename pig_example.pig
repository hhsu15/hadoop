/*define schema*/
ratings = LOAD '/user/maria_dev/ml-100k/u.data' AS (userID:int, movieID:int, rating:int, ratingTime:int);

/*define schema*/
metadata = LOAD '/user/maria_dev/ml-100k/u.item' USING PigStorage('|')
	AS (movieID:int, movieTitle:chararray, 
        releaseDate:chararray, 
        videoRelease:chararray,
        imdbLink:chararray);

/*get the fields you need and create a field for releaseTime*/
nameLookup = FOREACH metadata GENERATE movieID, movieTitle,
	ToUnixTime(ToDate(releaseDate, 'dd-MMM-yyyy')) AS releaseTime;

/* then group ratings by movie id*/
ratingsByMovie = Group ratings BY movieID;

/* get group of move id group and average ratings */
avgRatings = FOREACH ratingsByMovie GENERATE group AS movieID, AVG(ratings. rating) AS avgRating;

fiveStarMovies = FILTER avgRatings By avgRating > 4.0;

/* five star moveis data join nameLookup to get the movie name */
fiveStarsWithData = JOIN fiveStarMovies BY movieID, nameLookup BY movieID;

oldestFiveStarMovies = ORDER fiveStarsWithData BY nameLookup::releaseTime;

DUMP oldestFiveStarMovies;

