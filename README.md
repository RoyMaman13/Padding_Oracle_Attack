# Padding Oracle Attack
This project demonstrates a padding oracle attack on a ciphertext that was encrypted using the CBC (Cipher Block Chaining) encryption method. The project can decrypt the ciphertext without access to the encryption key through the padding oracle vulnerability.

### Getting Started
To decrypt a given ciphertext, run the ex1.py file with three required arguments: the ciphertext, the encryption key, and the IV (Initialization Vector) block.

Example Usage
```bash
py ex1.py 4e301349b6704658fcb5fb7dabf34e206e3e1223b86c1b4e360d69dcac04ac4e Aalenian 8487ffc596953c48
```
Arguments:
Ciphertext: The encrypted message to be decrypted.
Key: The encryption key used to encrypt the original message.
IV: The initialization vector used in the CBC encryption process.

### Testing
The project includes a test file, testEx1.py, which validates the decryption process against known inputs and outputs.

How to Run the Test
The test script reads inputs from input.txt.
The expected output is stored in output.txt.
To execute the test, run:
```bash
py testEx1.py
```
The script will compare the results with the expected output and print the results for verification.

### Files
ex1.py: Main script that performs the padding oracle attack decryption.
testEx1.py: Test script to verify correct decryption.
input.txt: Contains the test ciphertext, key, and IV for testing purposes.
output.txt: Contains the expected output for comparison.

### Prerequisites
Python 3.x
Any required libraries should be installed via pip.

### Notes
Make sure the ciphertext, key, and IV are in hexadecimal format as expected by the ex1.py script.
