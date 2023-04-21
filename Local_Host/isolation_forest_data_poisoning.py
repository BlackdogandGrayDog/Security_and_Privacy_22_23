#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 04:35:52 2023

@author: ericwei
"""

import csv
import mysql.connector
import pandas as pd
from sklearn.ensemble import IsolationForest

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "000000328",  # Replace with your root password
    "database": "healthcare",
}

connection = mysql.connector.connect(**db_config)

# Fetch data from the new table name
query = "SELECT * FROM cancer_prediction_data;"
df = pd.read_sql_query(query, connection)

connection.close()

# Isolation Forest
isolation_forest = IsolationForest(contamination=0.1, random_state=42)
isolation_forest.fit(df.drop(columns=['diagnosis']))

# Get anomaly scores and anomaly labels
anomaly_scores = isolation_forest.decision_function(df.drop(columns=['diagnosis']))
anomaly_labels = isolation_forest.predict(df.drop(columns=['diagnosis']))

# Add the anomaly labels to the dataframe
df['anomaly'] = anomaly_labels

# Drop all anomalies and create a new dataset
new_df = df[df['anomaly'] == 1].drop(columns=['anomaly'])
new_df.reset_index(drop=True, inplace=True)

print("New dataset without anomalies:")
print(new_df)

# Save cleaned data to a CSV file without the 'id' and 'anomaly' columns
new_df.drop(columns=['id']).to_csv("clean_cancer_prediction_data.csv", index=False)

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Drop the table if it exists
drop_table_query = """
DROP TABLE IF EXISTS clean_cancer_prediction_data;
"""
cursor.execute(drop_table_query)
connection.commit()

# Create the table with the new schema
create_table_query = """
CREATE TABLE IF NOT EXISTS clean_cancer_prediction_data (
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

csv_file_path = "clean_cancer_prediction_data.csv"
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        insert_query = """
        INSERT INTO clean_cancer_prediction_data (mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness, diagnosis)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, row)

    connection.commit()

cursor.close()
connection.close()

connection = mysql.connector.connect(**db_config)

# Fetch data from the new table name
query = "SELECT * FROM clean_cancer_prediction_data;"
df = pd.read_sql_query(query, connection)

connection.close()

print(df)
