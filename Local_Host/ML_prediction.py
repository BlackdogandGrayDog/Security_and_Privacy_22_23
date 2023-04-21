#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 05:15:16 2023

@author: ericwei
"""
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "000000328",  # Replace with your root password
    "database": "healthcare",
}

def load_data():
    connection = mysql.connector.connect(**db_config)
    query = "SELECT * FROM clean_cancer_prediction_data;"
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

def train_model():
    df = load_data()
    df = df.drop(columns=['id'])
    train_data, test_data, train_labels, test_labels = train_test_split(
        df.drop(columns=['diagnosis']), df['diagnosis'], test_size=0.1, random_state=42)
    
    scaler = StandardScaler()
    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)
    model = Sequential([
        Dense(128, activation='relu', input_shape=(train_data.shape[1],)),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    train_labels = train_labels.astype(int).astype(float)
    test_labels = test_labels.astype(int).astype(float)

    history = model.fit(train_data, train_labels, epochs=30, batch_size=16, validation_split=0.1)

    # Evaluate the performance of the model on the testing data
    loss, accuracy = model.evaluate(test_data, test_labels)
    print('Test accuracy:', accuracy)

    # Plot the training history
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(history.history['accuracy'], label='Train')
    ax1.plot(history.history['val_accuracy'], label='Validation')
    ax1.set_title('Model accuracy', fontweight='bold', fontsize = 15)
    ax1.set_xlabel('Epoch', fontweight='bold', fontsize = 15)
    ax1.set_ylabel('Accuracy', fontweight='bold', fontsize = 15)
    ax1.legend(loc='upper left')
    ax1.grid()

    ax2.plot(history.history['loss'], label='Train')
    ax2.plot(history.history['val_loss'], label='Validation')
    ax2.set_title('Model loss', fontweight='bold', fontsize = 15)
    ax2.set_xlabel('Epoch', fontweight='bold', fontsize = 15)
    ax2.set_ylabel('Loss', fontweight='bold', fontsize = 15)
    ax2.legend(loc='upper right')
    ax2.grid()

    plt.show()

    return model



def predict_diagnosis_proba(model, mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness):
    input_data = np.array([[mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness]])
    input_data = StandardScaler().fit_transform(input_data)
    prediction = model.predict(input_data)[0][0]
    return prediction

if __name__ == "__main__":
    model = train_model()

