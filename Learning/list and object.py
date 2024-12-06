from pyspark.sql import SparkSession
import os
os.environ["PYSPARK_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"
spark = SparkSession.builder\
    .master("local[5]")\
    .config("spark.driver.memory","4g")\
    .config("spark.executor.memory","4g")\
    .appName("Test").getOrCreate()
data_list = [(1, "Alice"), (2, "Bob"), (3, "Carol")]
data_object = [
    {"ID":"1","Name":"Praveen"},
    {"ID":"2","Name":"GK"},
    {"ID":"3","Name":"GKP"},
    {"ID":"4","Name":"PK"},
]
df_list = spark.createDataFrame(data_list, ["ID", "Name"])
df_object = spark.createDataFrame(data_object)
df_list.show()
df_object.show()
spark.stop()


#List: You might use a list when you need to store a collection of similar items
#Object: You would use an object when you need to encapsulate
#both data (attributes) and behavior (methods) for a particular entity
