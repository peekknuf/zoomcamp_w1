from pyspark.sql import SparkSession
import logging
import os

def ingest_data_to_postgresql(user, password, host, port, db, schema_name, data_directory):
    data_files = [f for f in os.listdir(data_directory) if f.endswith('.parquet')]

    try:
        spark = SparkSession.builder \
            .appName("DataToPostgreSQL") \
            .config("spark.driver.extraClassPath", "postgresql-42.6.0.jar") \
            .config("spark.executor.extraClassPath", "postgresql-42.6.0.jar") \
            .getOrCreate()

        for data_file in data_files:
            table_name = data_file.split('.')[0]
            data_df = spark.read.option("mergeSchema", "true").parquet(os.path.join(data_directory, data_file))

            data_df.write \
                .format("jdbc") \
                .option("url", f"jdbc:postgresql://{host}:{port}/{db}") \
                .option("dbtable", f"{schema_name}.{table_name}") \
                .option("user", user) \
                .option("password", password) \
                .mode("overwrite") \
                .save()

            logging.info(f"Data from {data_file} ingested to {schema_name}.{table_name} in PostgreSQL.")
    except Exception as e:
        logging.error(f"Error ingesting data to PostgreSQL: {str(e)}")

def main():
    user = "root"
    password = "root"
    host = "localhost"
    port = 5432
    db = "ny_taxi"
    schema_name = "public"
    data_directory = "/home/peek/ny_taxi_data"

    ingest_data_to_postgresql(user, password, host, port, db, schema_name, data_directory)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
