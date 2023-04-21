#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:58:09 2023

@author: ericwei
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
# Load the dataset
df = pd.read_csv('/Users/ericwei/Downloads/Breast_cancer_data.csv')

# Generate random data
num_random_samples = 500
random_data = np.random.rand(num_random_samples, df.shape[1] - 1) * 2.0 + 0.5
random_diagnosis = np.random.randint(0, 2, size=(num_random_samples, 1))
random_df = pd.DataFrame(np.hstack((random_data, random_diagnosis)), columns=df.columns)

# Concatenate the original DataFrame with the random data
df_extended = pd.concat([df, random_df], ignore_index=True)

# Split the extended DataFrame into training and testing data
test_data = df_extended.iloc[:100]
train_data = df_extended.iloc[100:]

def train_model_2(train_data, test_data):
    train_labels = train_data['diagnosis']
    test_labels = test_data['diagnosis']
    
    train_data = train_data.drop(columns=['diagnosis'])
    test_data = test_data.drop(columns=['diagnosis'])
    
    scaler = StandardScaler()
    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)
    
    # Model architecture
    model = Sequential([
        Dense(64, activation='relu', input_shape=(train_data.shape[1],)),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(8, activation='relu'),
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
    ax1.set_title('Model accuracy', fontweight='bold', fontsize=15)
    ax1.set_xlabel('Epoch', fontweight='bold', fontsize=15)
    ax1.set_ylabel('Accuracy', fontweight='bold', fontsize=15)
    ax1.legend(loc='upper left')
    ax1.grid()

    ax2.plot(history.history['loss'], label='Train')
    ax2.plot(history.history['val_loss'], label='Validation')
    ax2.set_title('Model loss', fontweight='bold', fontsize=15)
    ax2.set_xlabel('Epoch', fontweight='bold', fontsize=15)
    ax2.set_ylabel('Loss', fontweight='bold', fontsize=15)
    ax2.legend(loc='upper right')
    ax2.grid()

    plt.show()

    return model

# Train and plot the second model
if __name__ == "__main__":
    model_2 = train_model_2(train_data, test_data)



