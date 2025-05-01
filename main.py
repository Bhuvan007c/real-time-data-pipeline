from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType

spark = SparkSession.builder \
    .appName("KafkaSparkPostgres") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.postgresql:postgresql:42.2.27") \
    .getOrCreate()

schema = StructType() \
    .add("user_id", IntegerType()) \
    .add("event_type", StringType()) \
    .add("timestamp", StringType())

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "user-events") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

final_df = json_df.withColumn("timestamp", col("timestamp").cast(TimestampType()))

final_df.writeStream \
    .foreachBatch(lambda batch_df, batch_id: \
        batch_df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres:5432/events") \
            .option("dbtable", "user_activity") \
            .option("user", "postgres") \
            .option("password", "password") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()) \
    .outputMode("update") \
    .start() \
    .awaitTermination()
