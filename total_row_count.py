from pyspark.sql import SparkSession

def count_rows_in_tables():
    spark = SparkSession.builder \
        .appName("CountRowsInTables") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.extraClassPath", "postgresql-42.6.0.jar") \
        .config("spark.executor.extraClassPath", "postgresql-42.6.0.jar") \
        .getOrCreate()

    user = "root"
    password = "root"
    host = "localhost"
    port = 5432
    db = "ny_taxi"
    schema_name = "public"
    jdbc_url = f"jdbc:postgresql://{host}:{port}/{db}"
    properties = {"user": user, "password": password}
    total_row_count = 0
    years = range(2009, 2023)
    months = [str(month).zfill(2) for month in range(1, 13)]

    for year in years:
        for month in months:
            table_name = f"yellow_taxi_trips_{year}_{month}"
            try:
                table = spark.read.jdbc(url=jdbc_url, table=f"{schema_name}.{table_name}", properties=properties)
                count = table.count()
                total_row_count += count
                print(f"Table: {table_name}, Row Count: {count}")
            except Exception as e:
                print(f"Table {table_name} does not exist, skipping.")

    print(f"Total Row Count across all tables: {total_row_count}")
    spark.stop()

if __name__ == '__main__':
    count_rows_in_tables()
