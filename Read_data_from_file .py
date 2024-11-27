from pyspark.sql import SparkSession
import os
os.environ["PYSPARK_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"
spark = SparkSession.builder\
    .master("local[1]")\
    .config("spark.driver,memory","4g")\
    .config("spark.executor.memory","4g")\
    .appName("sparkexample").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
df= spark.read.options(header='True',inferSchema='False', delimiter=',') \
    .csv("C:\opt\sample_data.csv")
data = df
df.show()
df.printSchema()
spark.stop()

'''
Here we reading the single file from the path
we are not saving the data into the dataframe

Note:
inferSchema - it shows the table data types here we call it as schema.
master - it is the cluster manage. defines where the application will run 
and how resources are allocated.
(local[*]) - input for the cluster manager to run it on nodes.
sparkContext - it act as the connector to the spark cluster
'''
