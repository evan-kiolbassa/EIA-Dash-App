from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class CassandraDatabase:

    def __init__(self, contact_points, port, username, password, keyspace):
        auth_provider = PlainTextAuthProvider(
            username=username, password=password)
        self.cluster = Cluster(contact_points=contact_points,
                               port=port, auth_provider=auth_provider)
        self.session = self.cluster.connect(keyspace)

    def create_table(self, table_name, primary_key, columns):
        """
        Creates a new table in the database with the specified name, primary key, and columns.

        Args:
            table_name (str): The name of the table to create.
            primary_key (str): The primary key of the table.
            columns (list): A list of tuples representing the columns of the table. Each tuple should contain the name of the column and its data type.
        """
        column_definitions = ", ".join(
            [f"{column[0]} {column[1]}" for column in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions}, PRIMARY KEY ({primary_key}))"
        self.session.execute(query)

    def delete_table(self, table_name):
        """
        Deletes an existing table from the database.

        Args:
            table_name (str): The name of the table to delete.
        """
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.session.execute(query)

    def create_schema(self, schema_name, replication_factor, strategy_class='SimpleStrategy'):
        """
        Creates a new schema in the database with the specified
        name and replication factor.

        Args:
            schema_name (str): The name of the schema to create.
            replication_factor (int): The replication factor to use for the schema.
            strategy_class (str): The replication strategy class to use for the schema
              (default: 'SimpleStrategy').
        """
        query = f"CREATE KEYSPACE IF NOT EXISTS {schema_name} WITH REPLICATION = {{'class': '{strategy_class}', 'replication_factor': {replication_factor}}}"
        self.session.execute(query)

    def insert_data(self, table_name, data):
        """
        Inserts data into an existing table.

        Args:
            table_name (str): The name of the table to insert data into.
            data (dict): A dictionary representing the data to insert. The keys should
            correspond to the column names of the table, and the values should correspond to the data to insert.
        """
        column_names = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        self.session.execute(query, values)

    def update_data(self, table_name, primary_key_value, column_name, new_value):
        """
        Updates an existing row in a table with a new value.

        Args:
            table_name (str): The name of the table to update.
            primary_key_value (str): The value of the primary key of the row to update.
            column_name (str): The name of the column to update.
            new_value: The new value to set for the column.
        """
        query = f"UPDATE {table_name} SET {column_name} = %s WHERE {primary_key_value} = %s"
        self.session.execute(query, (new_value, primary_key_value))
