from pyspark.sql import SparkSession
from pyspark.sql.functions import when,col,expr,to_date
import os
os.environ ["PYSPARK_PYTHON"] = "C:/opt/PythonProject/.venv/Scripts/python.exe"
os.environ ["PYSPARK_DRIVER_PYTHON"] ="C:/opt/PythonProject/.venv/Scripts/python.exe"
spark = SparkSession\
        .builder\
        .master("local[5]")\
        .config("spark.driver.memory","4g")\
        .config("spark.executor.memory","4g")\
        .appName("Expression_transformation")\
        .getOrCreate()

df_large_file = spark.read.options(header="True").csv(r"C:\opt\CSV_input\random_employee_data.csv")

#expression_transformation
#exp_trans = df_large_file.withColumn("Adding",col("Salary")+col("Number"))
exp_trans = df_large_file\
        .withColumn("Adding",expr("cast(Salary+Number as INTEGER)"))\
        .withColumn("DOFB",to_date("DOB","yyyy-mm-dd"))\
        .withColumn("Salary_level",when(col("Salary") > 50000,"High").otherwise("Low"))\
        .withColumn("Area",when(col("City")=="San Francisco","RED")
                    .when(col("City")=="Chicago","BLUE").otherwise("GREEN"))\
        .withColumn("Salary_range",when(col("SALARY") > 70000, "High")\
                    .when(col("SALARY") > 50000, "Medium")\
                    .otherwise("Low"))

exp_trans.select("Name","ID","Adding","DOFB","Salary_level","Area").show()

#filter_transformation
df_filter = exp_trans.filter("Area = 'RED'")
df_filter.show()