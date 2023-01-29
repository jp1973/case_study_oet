from requests import get
from pyspark.sql import SparkSession

def download_file(URL):
    """ downloading file is separated into another function for the sake of better code understanding and maintainability"""
    url = URL
    r = get(url, allow_redirects=True)
    j_cont = str.encode(r.content.decode("utf-8").replace("[", "").replace("]", ""))
    open('mock_data.json', 'wb').write(j_cont)


def run_analysis(URL):
    download_file(URL) """ Downloading file"""
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("PySpark Read JSON") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    df = spark.read.json("./mock_data.json") # initializing data fraame
    print ('Printing schema of the recordset')
    df.printSchema()


    """ CTE expression is separated into variable for the sake of better readability. Data cleaning happens here"""
    cte_exp = "select * from EMP  where country RLIKE '^[A-Z].*'\
            and ip_address RLIKE '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'"
    df.createOrReplaceTempView("EMP")

    """select countries which have minimal amount of records on the list. Could be more then one"""
    sql_stmt = "with CTE as (" + cte_exp + ") select country, count(*) record_count from CTE group by country having count(*)\
     = (select count(*) as country_count from CTE group by country order by count(*) limit 1)"
    print('List of countries which have minimal occurences in the list')
    spark.sql(sql_stmt).show(50)

    """select countries which have maximal amount of records on the list. Could be more then one"""
    sql_stmt = "with CTE as (" + cte_exp + ") select country, count(*) record_count from CTE group by country having count(*)\
     = (select count(*) as country_count from CTE group by country order by count(*) desc limit 1)"
    print('List of countries which have maximal occurences in the list')
    spark.sql(sql_stmt).show(50)

    """ calculating amount of unique users( by email)"""
    sql_stmt = "with CTE as (" + cte_exp + ") select  count(distinct email) as unique_users from CTE"
    print('amount of unique users by email address')
    spark.sql(sql_stmt).show()


if __name__=="__main__":
    run_analysis('https://storage.googleapis.com/datascience-public/data-eng-challenge/MOCK_DATA.json')
