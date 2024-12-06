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

# Perform an inner join
join_transformation = sim_connection.join(sim_contract, on="ID", how="inner")

# Show the result of the join
join_transformation.show()

# Correct way to reference columns with an alias after join
update_transform = join_transformation\
    .withColumn("contract_enrich", when(
        (col("`Transaction date`") >= col("`Contract start date`")) &
        (col("`Transaction date`") < col("`Contract start date`")),
        "1"
    ).otherwise("0"))

filter_transform = update_transform.filter(col("contract_enrich") == "0")
filter_transform.show()


'''
sim_con = sim_connection.join(filter_transform, on="ID", how="inner")
sim_con.show()
simm_con = sim_con.withColumn("contract_enrich_fg",when(col("contract_enrich").isNotNull(),col("contract_enrich")).otherwise(lit(None)))
simm_con.show()
#simm_con.coalesce(1).write.option("header","true").csv(out_path)
'''