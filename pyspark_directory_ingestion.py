from pyspark.sql import SparkSession
import logging
import os


def ingest_data_to_postgresql(
    user, password, host, port, db, schema_name, data_directory
):
    try:
        spark = (
            SparkSession.builder.appName("DataToPostgreSQL")
            .config("spark.driver.extraClassPath", "postgresql-42.7.3.jar")
            .config("spark.executor.extraClassPath", "postgresql-42.7.3.jar")
            .config("spark.ui.port", "4041")
            .config("spark.driver.host", "localhost")
            .getOrCreate()
        )

        for data_file in os.listdir(data_directory):
            if data_file.endswith(".parquet"):
                table_name = os.path.splitext(data_file)[0]
                data_df = spark.read.option("mergeSchema", "true").parquet(
                    os.path.join(data_directory, data_file)
                )

                data_df.write.format("jdbc").option(
                    "url", f"jdbc:postgresql://{host}:{port}/{db}"
                ).option("dbtable", f"{schema_name}.{table_name}").option(
                    "user", user
                ).option("password", password).mode("overwrite").save()

                logging.info(
                    f"Data from {data_file} ingested to {schema_name}.{table_name} in PostgreSQL."
                )
    except Exception as e:
        logging.error(f"Error ingesting data to PostgreSQL: {str(e)}")


def main():
    user = "root"
    password = "1234"
    host = "172.27.49.79"
    port = 5432
    db = "ny_taxi"
    schema_name = "public"
    data_directory = "./ny_taxi_data/"

    ingest_data_to_postgresql(
        user, password, host, port, db, schema_name, data_directory
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
