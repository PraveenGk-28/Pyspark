from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os

os.environ ["PYSPARK_PYTHON"]="C:/opt/PythonProject/.venv/Scripts/python.exe"
os.environ ["PYSPARK_DRIVER_PYTHON"]="C:/opt/PythonProject/.venv/Scripts/python.exe"

class sparksession():
    def __init__(self):
        self.spark = SparkSession.builder.master('local[5]')\
        .config("spark.connector.memory","4g")\
        .config("spark.driver.memory","4g")\
        .appName("sparksessioncreate").getOrCreate()

    def take_spark(self):
        return self.spark

def main():
    make_spark = sparksession()
    spark = make_spark.take_spark()

if __name__ == '__main__':
    main()