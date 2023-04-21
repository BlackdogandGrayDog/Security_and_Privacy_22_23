# Local_Host

This folder contains the system built on a virtual machine for testing various types of attacks and their corresponding defense mechanisms. The primary purpose of the Local_Host folder is to enable testing and evaluation of the implemented security measures before deploying them to the cloud server.

## Contents

The Local_Host folder includes the following tests and defense systems:

1. **Code-Based Data Poisoning Attack**: This test simulates a data poisoning attack targeting the system's machine learning models. The corresponding defense mechanism involves utilizing the Isolation Forest algorithm to detect anomalies in the dataset and identify potential data poisoning attacks.

2. **Brute Force Attack for Web**: This test involves simulating a brute force attack on the web application's authentication system. The defense mechanism implemented in response to this attack includes monitoring and recording failed login attempts to detect potential brute force attacks, and terminating the session if a threshold of failed attempts is exceeded.

3. **SQL Injection Attack**: This test demonstrates a simulated SQL injection attack on the system's database. The defense system implemented to counter this attack involves monitoring and analyzing SQL queries to identify and prevent malicious SQL injection attempts.

4. **Firewall**: A firewall is implemented as part of the defense system to protect the Local_Host environment from unauthorized access and potential attacks.

5. **Brute Force Attack Detection**: This defense mechanism monitors and records failed login attempts, and if a specified threshold is exceeded, it identifies the activity as a potential brute force attack and terminates the session.

6. **Isolation Forest**: This algorithm is used to detect anomalies in the dataset, which can help identify potential data poisoning attacks and maintain the integrity of the machine learning models.

7. **Machine Learning Model Performance Testing**: This test evaluates the performance of the machine learning models under various attack scenarios and ensures the models are robust enough to withstand such attacks.

## Usage

To run the tests and defense mechanisms in the Local_Host folder, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the Local_Host folder.
3. Follow the instructions provided in each test and defense system's respective README file.

Please note that the Local_Host environment is designed for testing purposes only and should not be used for production deployments.
