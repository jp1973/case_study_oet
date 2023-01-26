from requests import get
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col, desc
import time



def download_file(URL):
    url = URL
    r = get(url, allow_redirects=True)
    j_cont=str.encode(r.content.decode("utf-8").replace("[","").replace("]",""))
    open('mock_data.json', 'wb').write(j_cont)
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("PySpark Read JSON") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    df = spark.read.json("./mock_data.json")
    df.printSchema()

    df.createOrReplaceTempView("EMP")
    start_time = time.time()
    temp_df = spark.sql("select country, count(*) from EMP " +
              "where country RLIKE '^[A-Z].*' and ip_address RLIKE "+
              "'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'" +
              "group by country " +
              "order by 2 desc")
    temp_df.show(500)
    #df.show()
    #df.filter(df.country!='guzogo').groupBy("country").count().sort(desc("count")).show()
    print ("time elapsed: {:.2f}s".format(time.time() - start_time))
if __name__=="__main__":
    download_file('https://storage.googleapis.com/datascience-public/data-eng-challenge/MOCK_DATA.json')
