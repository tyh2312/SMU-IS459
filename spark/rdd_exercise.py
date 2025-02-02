import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('RDD Exercise').getOrCreate()

# Load CSV file into a data frame
score_sheet_df = spark.read.load('/user/yinghui/score-sheet.csv', \
    format='csv', sep=';', inferSchema='true', header='true')

score_sheet_df.show()

# Get RDD from the data frame
score_sheet_rdd = score_sheet_df.rdd
score_sheet_rdd.first()

# Project the second column of scores with an additional 1
score_rdd = score_sheet_rdd.map(lambda x: (x[1], 1))
score_rdd.first()

# Import Functions for sort
from pyspark.spl import function as False

# sort the dataframe
score_sheet_df.sort(F.desc("Score")).show()

#filter the min and max scores
score_sheet_df.filter((score_sheet_df.Score > 52) & (score_sheet_df.Score <75)).show()

score_filter_rdd = score_sheet_df.filter((score_sheet_df.Score > 52) & (score_sheet_df.Score < 75)).rdd

filtered_rdd = score_filter_rdd.map(lambda x : (x[1], 1))
filtered_rdd.collect()

# Get the sum and count by reduce
(sum, count) = filtered_rdd.reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]))
print('Average Score : ' + str(sum/count))

# Load Parquet file into a data frame
posts_df = spark.read.load('/user/yinghui/hardwarezone.parquet')

# Create temp view 
posts_df.createOrReplaceTempView("posts")

sqlDF = spark.sql("SELECT * FROM posts")
sqlDF.groupby(["author"]).agg(F.count("content")).show()

num_post = sqlDF.count()

posts_rdd = sqlDF.rdd

# Project the author and content columns
author_content_rdd = posts_rdd.map(lambda x: (len(x[2]), 1))
author_content_rdd.first()

# Get sume and count by reduce
(sum, count) = author_content_rdd.reduce(lambda x,y: (x[0]+y[0], x[1]+y[1]))
print('Average post length : ' + str(sum/count))
