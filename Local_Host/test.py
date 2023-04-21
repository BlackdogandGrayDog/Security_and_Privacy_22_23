#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 02:48:28 2023

@author: ericwei
"""
import csv
import mysql.connector
import pandas as pd

# Replace these with your MySQL server credentials
db_config = {
    "host": "118.26.104.19",
    "user": "root",
    "password": "!Pw12123",  # Replace with your root password
    "database": "healthcare"
}

# Connect to the MySQL server
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS cancer_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mean_radius FLOAT NOT NULL,
    mean_texture FLOAT NOT NULL,
    mean_perimeter FLOAT NOT NULL,
    mean_area FLOAT NOT NULL,
    mean_smoothness FLOAT NOT NULL,
    diagnosis VARCHAR(2) NOT NULL
);
"""
cursor.execute(create_table_query)
connection.commit()

# Import the CSV file into the table
csv_file_path = "/Users/ericwei/Downloads/Breast_cancer_data.csv"
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        insert_query = """
        INSERT INTO cancer_data (mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness, diagnosis)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, row)

    connection.commit()

# Close the connection to the MySQL server
cursor.close()
connection.close()

# Connect to the MySQL server
connection = mysql.connector.connect(**db_config)

# Fetch data from the cancer_data table
query = "SELECT * FROM cancer_data;"
df = pd.read_sql_query(query, connection)

# Close the connection to the MySQL server
connection.close()

# Print the DataFrame
print(df)

