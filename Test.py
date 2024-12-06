from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os
import argparse

# Set environment for PySpark
os.environ["PYSPARK_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"



class sparkapp():
    def __init__(self,app_name : str):
        self.spark = SparkSession \
            .builder \
            .master('local[*]') \
            .config("spark.driver.memory", "8g") \
            .config("spark.executor.memory", "8g") \
            .appName(app_name) \
            .getOrCreate()

    def read_sim_connections():

        return spark.read.options(header='True').csv(r"C:/opt/CSV_input/sim_connections.csv")

    def read_sim_contracts():

        return spark.read.options(header='True').csv(r"C:/opt/CSV_input/sim_contracts.csv")

    def transformation(sim_connections,sim_contracts):

        df_trans = sim_connections.join (sim_contracs, on =['ID','Age'], how = 'INNER')
        df_trans.printSchema()
        #filter_df = df_trans.filter(col("sim_connections.Age") == 50)
        return df_trans

    def main():

        sim_connections = read_sim_connections()
        sim_contracts = read_sim_contracts()
        after_transformation = transformation(sim_connections,sim_contracts)

        sim_connections.show()
        sim_contracts.show()
        after_transformation.show()


if __name__ == '__main__':
    sparkapp("Apchespark")