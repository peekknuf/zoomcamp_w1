import unittest
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame


class TestDatabaseConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize SparkSession for testing
        cls.spark = (
            SparkSession.builder.appName("DatabaseConnectionTest")
            .config("spark.driver.extraClassPath", "postgresql-42.7.3.jar")
            .config("spark.executor.extraClassPath", "postgresql-42.7.3.jar")
            .master("local[*]")  # Use local mode for testing
            .getOrCreate()
        )

    @classmethod
    def tearDownClass(cls):
        # Stop SparkSession after testing
        cls.spark.stop()

    def test_database_connection(self):
        # Define PostgreSQL connection properties
        url = "jdbc:postgresql://172.27.49.79:5432/ny_taxi"

        # Create a sample DataFrame to write to the database
        sample_data = [("John", 30), ("Alice", 25), ("Bob", 35)]
        sample_df = self.spark.createDataFrame(sample_data, ["name", "age"])

        # Write the DataFrame to the database
        sample_df.write.jdbc(
            url=url,
            table="public.test_table",  # Define the table name
            mode="append",  # Overwrite the table if it exists
            properties={"user": "root", "password": "1234"},
        )

        # Read the written DataFrame back from the database
        read_back_df = self.spark.read.jdbc(
            url=url,
            table="public.test_table",
            properties={"user": "root", "password": "1234"},
        )

        # Assert that the DataFrame is not empty (indicating successful connection and write)
        self.assertIsInstance(read_back_df, DataFrame)
        self.assertNotEqual(
            read_back_df.count(),
            0,
            "Database connection failed or returned empty DataFrame",
        )


if __name__ == "__main__":
    unittest.main()
