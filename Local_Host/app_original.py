#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 01:10:26 2023

@author: ericwei
"""

from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import pandas as pd
import mysql.connector

app = Flask(__name__)
Bootstrap(app)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "000000328", 
    "database": "healthcare",
}

DEFAULT_USERNAME = 'a'
DEFAULT_PASSWORD = 'a'


@app.route('/')
def home():
    return 'Hello, this is the homepage!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == DEFAULT_USERNAME and request.form['password'] == DEFAULT_PASSWORD:
            return redirect(url_for('data'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error), 401
    return render_template('login.html', error=error)


@app.route('/data', methods=['GET'])
def data():
    # Connect to the MySQL server
    connection = mysql.connector.connect(**db_config)

    # Fetch data from the cancer_data table
    query = "SELECT * FROM cancer_prediction_data;"
    df = pd.read_sql_query(query, connection)

    # Close the connection to the MySQL server
    connection.close()

    # Pass the DataFrame to the template
    return render_template('data.html', data=df)


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('q', '')

    # Connect to the MySQL server
    connection = mysql.connector.connect(**db_config)

    # Fetch data from the cancer_data table
    query = f"SELECT * FROM cancer_prediction_data WHERE diagnosis LIKE '%{search_query}%';"
    df = pd.read_sql_query(query, connection)

    # Close the connection to the MySQL server
    connection.close()

    # Pass the DataFrame to the template
    return render_template('search.html', data=df)

# '; DROP TABLE cancer_data_prediction;--


@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        # Get the data from the form
        mean_radius = request.form['mean_radius']
        mean_texture = request.form['mean_texture']
        mean_perimeter = request.form['mean_perimeter']
        mean_area = request.form['mean_area']
        mean_smoothness = request.form['mean_smoothness']
        diagnosis = request.form['diagnosis']

        # Connect to the MySQL server
        connection = mysql.connector.connect(**db_config)

        # Insert the data into the cancer_prediction_data table
        query = "INSERT INTO cancer_prediction_data (mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness, diagnosis) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor = connection.cursor()
        cursor.execute(query, (mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness, diagnosis))

        # Commit the transaction and close the connection
        connection.commit()
        connection.close()

        # Redirect to the data page
        return redirect(url_for('data'))

    return render_template('data.html')



@app.route('/delete', methods=['POST'])
def delete_data():
    data_id = request.form['data_id']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Vulnerable DELETE statement using string formatting
    cursor.execute(f"DELETE FROM cancer_prediction_data WHERE id = {data_id};")

    connection.commit()
    connection.close()

    update_ids()

    return redirect(url_for('data'))


def update_ids():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM cancer_prediction_data ORDER BY id;")

    id_list = [row[0] for row in cursor.fetchall()]
    updated_id_list = list(range(1, len(id_list) + 1))

    for old_id, new_id in zip(id_list, updated_id_list):
        cursor.execute("UPDATE cancer_prediction_data SET id = %s WHERE id = %s;", (new_id, old_id))

    connection.commit()
    connection.close()
    
    

if __name__ == '__main__':
    app.run(debug=True)
