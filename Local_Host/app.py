#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 00:18:58 2023

@author: ericwei
"""

from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
import pandas as pd
import mysql.connector
import ML_prediction as ml

app = Flask(__name__)
Bootstrap(app)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "000000328",  # Replace with your root password
    "database": "healthcare",
}

DEFAULT_USERNAME = 'a'
DEFAULT_PASSWORD = 'a'


@app.route('/')
def home():
    return redirect(url_for('data'))


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
    query = request.args.get('q')
    safe_query = f"%{query}%"

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query_string = f"SELECT * FROM cancer_prediction_data WHERE diagnosis LIKE %s;"
    cursor.execute(query_string, (safe_query,))

    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    connection.close()

    return render_template('search.html', data=rows, columns=columns)


@app.route('/add', methods=['GET', 'POST'])
def add_data():
    # Connect to the MySQL server
    connection = mysql.connector.connect(**db_config)

    if request.method == 'POST':
        # Get the data from the form
        mean_radius = request.form['mean_radius']
        mean_texture = request.form['mean_texture']
        mean_perimeter = request.form['mean_perimeter']
        mean_area = request.form['mean_area']
        mean_smoothness = request.form['mean_smoothness']
        diagnosis = request.form['diagnosis']

        # Validate the data
        numeric_columns = ['mean_radius', 'mean_texture', 'mean_perimeter', 'mean_area', 'mean_smoothness']
        values = [float(mean_radius), float(mean_texture), float(mean_perimeter), float(mean_area), float(mean_smoothness)]
        df = pd.read_sql_query("SELECT * FROM cancer_prediction_data;", connection)
        Q1 = df[numeric_columns].quantile(0.25)
        Q3 = df[numeric_columns].quantile(0.75)
        IQR = Q3 - Q1
        iqr_multiplier = 1.5
        for column, value, q1, q3 in zip(numeric_columns, values, Q1, Q3):
            if value < (q1 - iqr_multiplier * IQR[column]) or value > (q3 + iqr_multiplier * IQR[column]):
                error = f"{column}: {value} is outside the normal range ({q1 - iqr_multiplier * IQR[column]} - {q3 + iqr_multiplier * IQR[column]})"
                return render_template('data.html', data=df, error=error), 400

        # Insert the data into the cancer_prediction_data table
        query = "INSERT INTO cancer_prediction_data (mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness, diagnosis) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor = connection.cursor()
        cursor.execute(query, (mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness, diagnosis))

        # Commit the transaction
        connection.commit()

    # Fetch data from the cancer_data table
    df = pd.read_sql_query("SELECT * FROM cancer_prediction_data;", connection)

    # Close the connection to the MySQL server
    connection.close()

    # Pass the DataFrame to the template
    return render_template('data.html', data=df)

        
        

@app.route('/delete', methods=['POST'])
def delete_data():
    data_id = request.form['data_id']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM cancer_prediction_data WHERE id = %s;", (data_id,))

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
    
    

def get_columns_names():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SHOW COLUMNS FROM cancer_prediction_data;")
    columns = [column[0] for column in cursor.fetchall()]
    connection.close()
    return columns

@app.route('/update', methods=['POST'])
def update_data():
    data = request.get_json()
    data_id = data['id']
    column_index = int(data['column'])
    new_value = data['value']

    columns = get_columns_names()
    column_name = columns[column_index]
    numeric_columns = ['mean_radius', 'mean_texture', 'mean_perimeter', 'mean_area', 'mean_smoothness']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(f"SELECT {column_name} FROM cancer_prediction_data WHERE id = %s;", (data_id,))
    old_row = cursor.fetchone()

    if old_row is not None:
        old_value = old_row[0]
    else:
        connection.close()
        return jsonify({'error': 'Row not found', 'oldValue': None})

    if column_name in numeric_columns:
        value = float(new_value)
        df = pd.read_sql_query("SELECT * FROM cancer_prediction_data;", connection)
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)
        IQR = Q3 - Q1
        iqr_multiplier = 1.5
        if value < (Q1 - iqr_multiplier * IQR) or value > (Q3 + iqr_multiplier * IQR):
            error = f"{column_name}: {value} is outside the normal range ({Q1 - iqr_multiplier * IQR}, {Q3 + iqr_multiplier * IQR})"
            connection.close()
            return jsonify({'error': error, 'oldValue': old_value})
        else:
            cursor.execute(f"UPDATE cancer_prediction_data SET {column_name} = %s WHERE id = %s;", (new_value, data_id))
    else:
        cursor.execute(f"UPDATE cancer_prediction_data SET {column_name} = %s WHERE id = %s;", (new_value, data_id))

    connection.commit()
    connection.close()
    return jsonify({})



@app.route('/predict_diagnosis', methods=['GET', 'POST'])
def predict_diagnosis():
    if request.method == 'POST':
        mean_radius = float(request.form['mean_radius'])
        mean_texture = float(request.form['mean_texture'])
        mean_perimeter = float(request.form['mean_perimeter'])
        mean_area = float(request.form['mean_area'])
        mean_smoothness = float(request.form['mean_smoothness'])
        model = ml.train_model()
        prediction = ml.predict_diagnosis_proba(model, mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness)
        return render_template('predict.html', prediction=prediction)

    return render_template('predict.html')



if __name__ == '__main__':
    app.run(debug=True)


