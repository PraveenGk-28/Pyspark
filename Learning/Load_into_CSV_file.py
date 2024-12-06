from pyspark.sql import SparkSession
import os
os.environ ["PYSPARK_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"
os.environ ["PYSPARK_DRIVER_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"


spark = SparkSession\
    .builder\
    .master("local[5]")\
    .config("spark.driver.memory","4g")\
    .config("spark.executor.memory","4g")\
    .appName("load_into_csv_file")\
    .getOrCreate()

csv_read = spark.read.options(header='True').csv(r"C:\opt\CSV_input\sample_data.csv")

csv_read.show()

output_path = r"C:\opt\CSV_output"

#csv_read.coalesce(1).write.options(header='True').mode("overwrite").csv(output_path)
csv_read.coalesce(1).write.option("header", "true").csv(output_path)

spark.stop()

'''
while learning i did this mistake csv_read is already a data frame.
i could not a create the data frame by using below
df = spark.createDataFrame(csv_read)

csv_read_write = spark.read.options(header='True').csv("C:\opt\Export_data.csv")

csv_read_write.show()
'''

spark.stop()

