import subprocess
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes

inputs = []
outputs = []

i = 0
# Step 2: Load inputs and outputs from files
with open("inputs.txt", "r") as inputs_file:
    inputs = inputs_file.read().splitlines()

with open("outputs.txt", "r") as outputs_file:
    expected_outputs = outputs_file.read().splitlines()

# Step 3: Run the program ex1.py with each input and compare outputs
total_tests = len(inputs)
success_count = 0
failed_tests = []

prints_success = []
prints_fail = []
for i in range(total_tests):
    input_data = inputs[i].split()
    expected_output = expected_outputs[i]
    ciphertext = bytes.fromhex(input_data[0])
    myKey = input_data[1].encode('utf-8')
    myIV = bytes.fromhex(input_data[2])

    myCipher = DES.new(myKey, DES.MODE_CBC, myIV)
    decrypted_plaintext = unpad(myCipher.decrypt(ciphertext), 8).decode('utf-8')

    # Execute ex1.py and capture the output
    cmd = ['python', 'ex1.py', input_data[0], input_data[1], input_data[2]]
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8').strip()
    except Exception as e:
        output = "Your program crashed."
    # Compare the output with the expected output
    if decrypted_plaintext == expected_output and output == expected_output:
        prints_success.append(f"Test {i+1}/{total_tests} - SUCCESS. Expected: {expected_output}. Got: {output}")
        success_count += 1
    else:
        prints_fail.append(f"Test {i+1}/{total_tests} - FAIL. Expected: {expected_output}, Got: {output}")
        failed_tests.append(i+1)

    if i % 5 == 0:
        for i in range(len(prints_success)):
            print(prints_success[i])

        for i in range(len(prints_fail)):
            print(prints_fail[i])
        
        prints_success = []
        prints_fail = []
# Print overall test results
print(f"\n****Total Tests: {success_count}/{total_tests} - SUCCEEDED****")

# Print failed test inputs
if failed_tests:
    print("\nFailure inputs:")
    print(", ".join(str(test) for test in failed_tests))
