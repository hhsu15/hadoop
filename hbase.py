from starbase import Connection

# create connection
c = Connection('127.0.0.1', '8000')

# create a table called rartings
ratings = c.table('ratings')

# drop table if exists
if ratings.exists():
    print("Dropping existing ratings table")
    ratings.drop()

# create a column family called raitng within ratings table
# this is like creating a key in the schema
ratings.create('rating')

print("Parsing the ml-100k ratings data...\n")
ratingFile = open("Downloads/ml-100k/u.data", "r")

# create a batch object
batch = ratings.batch()

# update the batch given each row
for line in ratingFile:
        (userID, movieID, rating, timestamp) = line.split()
        batch.update(userID, {'rating':{movieID: rating}})

ratingFile.close()

print("Committing ratings data to HBase via REST service")
batch.commit(finalize=True)

print("Get back raitngs for some users...")
print("Ratings for user ID 1:")
print(ratings.fetch("1"))
print("Ratings for user ID 33:")
print(ratings.fetch("33"))

