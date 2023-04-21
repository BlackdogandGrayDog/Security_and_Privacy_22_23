#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 02:10:20 2023

@author: ericwei
"""

import itertools
import string
import mysql.connector
from sys import exit

# Change these to your MySQL credentials
USERNAME = "root"
PASSWORD = "000000328"
DB_NAME = "healthcare"

def create_failed_login_attempts_table():
    connection = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        password=PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS failed_login_attempts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME NOT NULL,
        user VARCHAR(255) NOT NULL,
        ip_address VARCHAR(255) NOT NULL
    );
    """)
    connection.commit()
    cursor.close()
    connection.close()

def insert_failed_login_attempt(user, ip_address):
    connection = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        password=PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    cursor.execute("INSERT INTO failed_login_attempts (timestamp, user, ip_address) VALUES (NOW(), %s, %s)", (user, ip_address))
    connection.commit()
    cursor.close()
    connection.close()

def count_failed_login_attempts(user, ip_address):
    connection = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        password=PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM failed_login_attempts WHERE user = %s AND ip_address = %s AND timestamp > (NOW() - INTERVAL 1 HOUR);", (user, ip_address))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count

def try_connection(password, user, ip_address):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=USERNAME,
            password=password,
            database=DB_NAME
        )
        print(f"Password found: {password}")
        return True
    except mysql.connector.Error as err:
        if err.errno == 1045:  # Access denied error
            failed_attempts = count_failed_login_attempts(user, ip_address)
            if failed_attempts >= 3:
                print(f"Too many failed login attempts from IP address {ip_address} for user {user}")
                return "stop_execution"

            insert_failed_login_attempt(user, ip_address)
            return False
        else:
            print(f"Unexpected error: {err}")
            return False

def brute_force(min_length, max_length, user, ip_address):
    characters = string.digits
    for length in range(min_length, max_length + 1):
        for combination in itertools.product(characters, repeat=length):
            password = "".join(combination)
            result = try_connection(password, user, ip_address)
            if result == "stop_execution":
                return
            elif result:
                return

if __name__ == "__main__":
    create_failed_login_attempts_table()
    min_length = 9
    max_length = 9
    user = "root"
    ip_address = "127.0.0.1"  # Replace with the IP address you want to track
    brute_force(min_length, max_length, user, ip_address)
