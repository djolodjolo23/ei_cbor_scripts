import cbor2
import random
import uuid
import matplotlib.pyplot as plt

from read_cbor_and_plot import timestamps


def add_noise_to_data(data, noise_level):
    return [value + random.uniform(-noise_level, noise_level) for value in data]

def read_cbor_file(file_path):
    with open(file_path, 'rb') as file:
        data = cbor2.load(file)
    return data


sensor_data = read_cbor_file("TEST_TRIANGLE.5aevcvir.cbor")
new_values = []
timestamps = []
start_time = 10.0

for entry in sensor_data['payload']['values']:
    acc_x, acc_y, acc_z = add_noise_to_data(entry[0:3], 5)
    gyro_x, gyro_y, gyro_z = add_noise_to_data(entry[3:6], 30)
    new_values.append([acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z])
    timestamps.append(start_time)
    start_time += sensor_data['payload']['interval_ms']

# Save as a new CBOR file
new_sensor_data = {
    "protected": sensor_data["protected"],
    "signature": sensor_data["signature"],

    "payload": {
        "device_name": sensor_data["payload"]["device_name"],
        "device_type": sensor_data["payload"]["device_type"],
        "interval_ms": sensor_data['payload']['interval_ms'],
        "sensors": sensor_data["payload"]["sensors"],
        "values": new_values,
    }
}

filename = f"triangle_artificial_data_{uuid.uuid4().hex}.cbor"
with open(filename, 'wb') as file:
    cbor2.dump(new_sensor_data, file)

gyro_x = [entry[3] for entry in new_values]
gyro_y = [entry[4] for entry in new_values]
gyro_z = [entry[5] for entry in new_values]

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