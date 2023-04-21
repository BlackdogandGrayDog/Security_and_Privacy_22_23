#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 05:15:16 2023

@author: ericwei
"""

import csv
import mysql.connector
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from model_encode import encrypt_parameters, decrypt
from phe import paillier

# Noise confusion
def apply_noise(x, epsilon=0.1):
    # Generate random numbers in the range [-epsilon, epsilon].
    noise = np.random.uniform(-epsilon, epsilon, x.shape)
    # Adding disturbance noise
    x = x + noise
    # Cropping the input values to a suitable range
    x = np.clip(x, 0.0, 1.0)
    return x

db_config = {
    "host": "118.26.104.19",
    "user": "root",
    "password": "!Pw12123",  # Replace with your root password
    "database": "healthcare",
}

connection = mysql.connector.connect(**db_config)

# Fetch data from the new table name
query = "SELECT * FROM cancer_prediction_data;"
df = pd.read_sql_query(query, connection)

connection.close()
# Split the data into training and testing sets
train_data, test_data, train_labels, test_labels = train_test_split(
    df.drop(columns=['diagnosis']), df['diagnosis'], test_size=0.1, random_state=42)

train_data = apply_noise(train_data,0.01)
test_data = apply_noise(test_data,0.01)

# Preprocess the data by standardizing the features
scaler = StandardScaler()
train_data = scaler.fit_transform(train_data)
test_data = scaler.transform(test_data)

# Define the architecture of your deep neural network
model = Sequential([
    Dense(128, activation='relu', input_shape=(train_data.shape[1],)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Convert the labels to integers and then to float
train_labels = train_labels.astype(int).astype(float)
test_labels = test_labels.astype(int).astype(float)



# Train the model on the training data
history = model.fit(train_data, train_labels, epochs=30, batch_size=16, validation_split=0.1)

# Encrypted preservation of models
encrypt_parameters(model)


# Evaluate the performance of the model on the testing data
loss, accuracy = model.evaluate(test_data, test_labels)
print('Test accuracy:', accuracy)

# Plot the training history
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(history.history['accuracy'], label='Train')
ax1.plot(history.history['val_accuracy'], label='Validation')
ax1.set_title('Model accuracy')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend(loc='upper left')

ax2.plot(history.history['loss'], label='Train')
ax2.plot(history.history['val_loss'], label='Validation')
ax2.set_title('Model loss')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.legend(loc='upper right')

plt.show()

# Plot the test results
# Get the predicted labels from the model

# Model decryption reading
model = decrypt()

predicted_labels = model.predict(test_data)

# Convert the predicted probabilities to binary labels
predicted_labels_binary = np.where(predicted_labels > 0.5, 1, 0)

# Plot the actual test labels as blue dots
plt.scatter(range(len(test_labels)), test_labels, color='blue', label='Actual Labels')

# Plot the predicted labels as red dots
plt.scatter(range(len(predicted_labels_binary)), predicted_labels_binary, color='red', label='Predicted Labels', alpha=0.5)

# Add labels to the axes and a legend
plt.xlabel('Sample Index')
plt.ylabel('Label')
plt.legend()
plt.title('Actual vs. Predicted Labels')

# Display the plot
plt.show()

