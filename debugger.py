import os

# Force correct Python + Java connection
os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FINAL_FIX") \
    .master("local[1]") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .config("spark.python.worker.reuse", "false") \
    .config("spark.network.timeout", "600s") \
    .getOrCreate()

rdd = spark.sparkContext.parallelize([1,2,3,4])
print(rdd.map(lambda x: x * 2).collect())