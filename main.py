import cbor2
import matplotlib.pyplot as plt

# Function to read CBOR file
def read_cbor_file(file_path):
    with open(file_path, 'rb') as file:
        data = cbor2.load(file)
    return data

# Replace with your CBOR file path
file_path = 'djordje_circle.5aeoupfd.s3.cbor'
sensor_data = read_cbor_file(file_path)

# Inspect the data structure
print(sensor_data.keys())  # Should show: protected, signature, values

# Extracting the data from "values"
timestamps = []
acc_x, acc_y, acc_z = [], [], []
gyro_x, gyro_y, gyro_z = [], [], []

# Assuming each entry in "values" is a list where:
# [timestamp, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]
for entry in sensor_data['payload']['values']:
    timestamps.append(entry[0])  # Time
    acc_x.append(entry[1])       # Accelerometer X
    acc_y.append(entry[2])       # Accelerometer Y
    acc_z.append(entry[3])       # Accelerometer Z
    gyro_x.append(entry[4])      # Gyroscope X
    gyro_y.append(entry[5])      # Gyroscope Y
    gyro_z.append(entry[6])      # Gyroscope Z

# Convert timestamps from milliseconds to seconds if needed
timestamps = [t / 1000 for t in timestamps]

# Plot accelerometer data
plt.figure(figsize=(10, 6))
plt.plot(timestamps, acc_x, label='Acc X', alpha=0.7)
plt.plot(timestamps, acc_y, label='Acc Y', alpha=0.7)
plt.plot(timestamps, acc_z, label='Acc Z', alpha=0.7)
plt.xlabel("Time (s)")
plt.ylabel("Accelerometer (m/s²)")
plt.title("Accelerometer Data")
plt.legend()
plt.grid(True)
plt.show()

# Plot gyroscope data
plt.figure(figsize=(10, 6))
plt.plot(timestamps, gyro_x, label='Gyro X', alpha=0.7)
plt.plot(timestamps, gyro_y, label='Gyro Y', alpha=0.7)
plt.plot(timestamps, gyro_z, label='Gyro Z', alpha=0.7)
plt.xlabel("Time (s)")
plt.ylabel("Gyroscope (°/s)")
plt.title("Gyroscope Data")
plt.legend()
plt.grid(True)
plt.show()
