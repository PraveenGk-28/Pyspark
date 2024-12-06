from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os

# Set environment for PySpark
os.environ["PYSPARK_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"


class sparkapp():
    def __init__(self, app_name: str):
        self.spark = SparkSession \
            .builder \
            .master('local[*]') \
            .config("spark.driver.memory", "8g") \
            .config("spark.executor.memory", "8g") \
            .appName(app_name) \
            .getOrCreate()

    def get_spark(self):
        return self.spark


def read_sim_connections(spark):
    return spark.read.options(header='True').csv(r"C:/opt/CSV_input/sim_connections.csv")


def read_sim_contracts(spark):
    return spark.read.options(header='True').csv(r"C:/opt/CSV_input/sim_contracts.csv")


def transformation(sim_connections, sim_contracts):
    sim_con_re = sim_connections.withColumnRenamed("Age", "Age_cons")
    sim_cont_re = sim_contracts.withColumnRenamed("Age", "Age_cont")
    df_trans = sim_con_re.join(sim_cont_re, on=['ID'], how='INNER')  # join condition
    filter_df = df_trans.filter(col("Age_cons") == 50)  # filter condition
    null_value = filter_df.fillna({'Age_cont': 0})  # this replaces null value with 0
    set_value = null_value.withColumn("Age_cont", when(col("Age_cont") >= 50, 50)
                                      .when(col("Age_cont") <= 30, 30)
                                      .otherwise(col("Age_cont")))

    return set_value


def file_write(after_transformation, outputpath):
    # Write the data to the specified path
    after_transformation.coalesce(1).write.option("header", "True").csv(outputpath)


def main():
    app = sparkapp("Apchespark")
    spark = app.get_spark()

    # Reading input files
    sim_connections = read_sim_connections(spark)
    sim_contracts = read_sim_contracts(spark)

    # Show the data for verification
    sim_connections.show()
    sim_contracts.show()

    # Perform transformation
    after_transformation = transformation(sim_connections, sim_contracts)

    # Count the resulting dataframe
    df_count = after_transformation.count()
    after_transformation.show()
    print(f"Count: {df_count}")

    # Write the output to the given path
    file_write(after_transformation, r"C:/opt/file")


if __name__ == '__main__':
    main()