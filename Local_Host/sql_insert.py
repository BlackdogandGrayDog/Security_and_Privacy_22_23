#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 05:49:49 2023

@author: ericwei
"""
import csv
import mysql.connector
import pandas as pd

# db_config = {
#     "host": "118.26.104.19",
#     "user": "root",
#     "password": "!Pw12123",  # Replace with your root password
#     "database": "healthcare",
# }

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "000000328",  # Replace with your root password
    "database": "healthcare",
}

# connection = mysql.connector.connect(**db_config)
# cursor = connection.cursor()

# # Create the table if it doesn't exist, using the new table name
# create_table_query = """
# CREATE TABLE IF NOT EXISTS cancer_prediction_data (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     mean_radius FLOAT NOT NULL,
#     mean_texture FLOAT NOT NULL,
#     mean_perimeter FLOAT NOT NULL,
#     mean_area FLOAT NOT NULL,
#     mean_smoothness FLOAT NOT NULL,
#     diagnosis VARCHAR(2) NOT NULL
# );
# """
# cursor.execute(create_table_query)
# connection.commit()

# csv_file_path = "/Users/ericwei/Downloads/Breast_cancer_data.csv"
# with open(csv_file_path, "r") as csv_file:
#     csv_reader = csv.reader(csv_file)
#     next(csv_reader)  # Skip the header row

#     for row in csv_reader:
#         insert_query = """
#         INSERT INTO cancer_prediction_data (mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness, diagnosis)
#         VALUES (%s, %s, %s, %s, %s, %s);
#         """
#         cursor.execute(insert_query, row)

#     connection.commit()

# cursor.close()
# connection.close()

connection = mysql.connector.connect(**db_config)

# Fetch data from the new table name
query = "SELECT * FROM cancer_prediction_data;"
df = pd.read_sql_query(query, connection)

connection.close()

print(df)
