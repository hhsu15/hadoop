CREATE VIEW IF NOT EXISTS topRatedMovie AS
SELECT movieID, COUNT(movieID) as ratingCount, AVG(rating) as avgRating
FROM ratings
GROUP BY movieID
ORDER BY avgRating DESC;

SELECT n.title, avgRating
FROM topRatedMovie t JOIN names n ON t.movieID = n.movieID
WHERE ratingCount >= 10;
