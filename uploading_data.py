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
    url = params.url

    spark = SparkSession.builder \
        .appName("ParquetToPostgreSQL") \
        .config("spark.driver.extraClassPath", "postgresql-42.6.0.jar") \
        .config("spark.executor.extraClassPath", "postgresql-42.6.0.jar") \
        .getOrCreate()
    
    if url.endswith('.parquet'):
        parquet = 'output.parquet'

        download_command = f"wget {url} -O {parquet}"
        result = subprocess.run(download_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            parquet_file = parquet
            print(f"Parquet file downloaded to: {parquet_file}")

            parquet_df = spark.read.format("parquet").load(parquet_file)
            print("Parquet data loaded successfully.")

            postgres_options = {
                "url": f"jdbc:postgresql://{host}:{port}/{db}",
                "dbtable": f"public.{table_name}",
                "user": user,
                "password": password  # Removed curly braces
            }

            parquet_df.write \
                .format("jdbc") \
                .option("url", postgres_options["url"]) \
                .option("dbtable", postgres_options["dbtable"]) \
                .option("user", postgres_options["user"]) \
                .option("password", postgres_options["password"]) \
                .mode("overwrite")  \
                .save()

            print("Data written to PostgreSQL successfully.")

        else:
            print("Error downloading the Parquet file:", result.stderr)
    else:
        print("The URL does not point to a parquet file.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)
