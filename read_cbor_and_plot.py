import cbor2
import matplotlib.pyplot as plt

def read_cbor_file(file_path):
    with open(file_path, 'rb') as file:
        data = cbor2.load(file)
    return data

file_path = 'TEST_TRIANGLE.5aevcvir.cbor'
sensor_data = read_cbor_file(file_path)

print(sensor_data.keys())
timestamps = []
acc_x, acc_y, acc_z = [], [], []
gyro_x, gyro_y, gyro_z = [], [], []

interval_ms = 10.0
current_timestamp = 0


for entry in sensor_data['payload']['values']:
    timestamps.append(current_timestamp)  # Time
    acc_x.append(entry[0])       # Accelerometer X
    acc_y.append(entry[1])       # Accelerometer Y
    acc_z.append(entry[2])       # Accelerometer Z
    gyro_x.append(entry[3])      # Gyroscope X
    gyro_y.append(entry[4])      # Gyroscope Y
    gyro_z.append(entry[5])      # Gyroscope Z
    current_timestamp += interval_ms

timestamps = [t / 1000 for t in timestamps]

"""
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
"""