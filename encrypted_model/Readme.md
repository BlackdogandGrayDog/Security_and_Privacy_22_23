## Neural Network Models and Data Privacy Defense
	## Neural Network Model Training and Inference File ML_prediction.py
		File containing data reading, training, encryption, decryption, effect presentation and inference functions.
		The file is updated online by pulling data from the cloud database.
		The simulation of data attacks on the model can be done by changing the data in the cloud.

	## Encryption and decryption algorithm file model_encode.py
		The encode function uses the Fernet library to generate and distribute the public and private keys and save the model.
		The decode function decrypts the model by reading the local private key.

	## Multi-party computation simulation SMC.py
		Three work objects, A, B and C, are established in this project. Parties A and B each initialize their own parameters. Party C generates the secret key pair and distributes the public key and obtains the encryption gradient, decrypts it, and then returns A and B