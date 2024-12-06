from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os

# Set environment for PySpark
os.environ["PYSPARK_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"

# Create Spark session
spark = SparkSession\
    .builder\
    .master('local[*]')\
    .config("spark.driver.memory", "8g")\
    .config("spark.executor.memory", "8g")\
    .appName("Update_strategy")\
    .getOrCreate()

# Load CSV data
sim_connection = spark.read.options(header='True').csv(r"C:/opt/CSV_input/sim_connections.csv")
sim_contract = spark.read.options(header='True').csv(r"C:/opt/CSV_input/sim_contracts.csv")

sim_connection.createOrReplaceTempView("sim_cons")
sim_contract.createOrReplaceTempView("sim_con")

spark.sql("SELECT a.*,b.* FROM sim_cons a INNER JOIN sim_con b ON a.ID = b.ID WHERE a.age >=45 "
          "and a.`transaction date` >= b.`contract start date` and a.`transaction date` < b.`contract end date` ").show(100)