import argparse
from pyspark.sql import SparkSession
import subprocess


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    schema_name = params.schema_name
    url = params.url

    spark = (
        SparkSession.builder.appName("DataToPostgreSQL")
        .config("spark.driver.extraClassPath", "postgresql-42.6.0.jar")
        .config("spark.executor.extraClassPath", "postgresql-42.6.0.jar")
        .config("spark.ui.port", "4041")
        .config("spark.driver.host", "localhost")
        .getOrCreate()
    )

    if url.endswith(".csv"):
        file_format = "csv"
    elif url.endswith(".parquet"):
        file_format = "parquet"
    else:
        print("Unsupported file format. Supported formats are CSV and Parquet.")
        return

    file_name = "output." + file_format
    download_command = f"wget {url} -O {file_name}"
    result = subprocess.run(
        download_command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode == 0:
        print(f"{file_format.upper()} file downloaded to: {file_name}")

        data_df = spark.read.format(file_format)

        if file_format == "csv":
            data_df = data_df.option("header", "true")  # If the CSV has a header
            data_df = data_df.option("inferSchema", "true")  # Infer the schema

        data_df = data_df.load(file_name)

        data_df.write.format("jdbc").option(
            "url", f"jdbc:postgresql://{host}:{port}/{db}"
        ).option("dbtable", f"{schema_name}.{table_name}").option("user", user).option(
            "password", password
        ).mode("append").save()

        print(f"Data written to {schema_name}.{table_name} in PostgreSQL.")

    else:
        print(f"Error downloading the {file_format.upper()} file:", result.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest data to PostgreSQL")

    parser.add_argument("--user", required=True, help="user name for PostgreSQL")
    parser.add_argument("--password", required=True, help="password for PostgreSQL")
    parser.add_argument("--host", required=True, help="host for PostgreSQL")
    parser.add_argument("--port", required=True, help="port for PostgreSQL")
    parser.add_argument("--db", required=True, help="database name for PostgreSQL")
    parser.add_argument(
        "--table_name",
        required=True,
        help="name of the table where we will write the results to",
    )
    parser.add_argument("--schema_name", required=True, help="name of the schema")
    parser.add_argument(
        "--url", required=True, help="URL of the data file (CSV or Parquet)"
    )
    args = parser.parse_args()

    main(args)
