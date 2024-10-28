import cbor2
import random
import uuid
import os


def add_variable_noise(value, min_noise, max_noise, min_value, max_value):
    normalized = (abs(value) - min_value) / (max_value - min_value)
    noise_level = min_noise + normalized * (max_noise - min_noise)
    return value + random.uniform(-noise_level, noise_level)


def add_noise_to_data(data, min_noise, max_noise):
    min_value, max_value = min(data), max(data)
    return [add_variable_noise(value, min_noise, max_noise, min_value, max_value) for value in data]

def read_cbor_file(file_path):
    with open(file_path, 'rb') as file:
        data = cbor2.load(file)
    return data

sensor_data = read_cbor_file("TEST_UNKOWN.5af8d3ip.cbor")
name = "unknown"
version = "v6"

root_dir = f'artificial_data_{version}'
sub_dir = os.path.join(root_dir, f'{name}_artificial_data_{version}')
readme_path = os.path.join(root_dir, 'README.md')
os.makedirs(sub_dir, exist_ok=True)

min_noise_acc = 0.01
max_noise_acc = 1
min_noise_gyro = 0.01
max_noise_gyro = 1
max_shift = 70

for i in range(1000):
    new_values = []
    timestamps = []
    start_time = 10.0

    for entry in sensor_data['payload']['values']:
        acc_x, acc_y, acc_z = add_noise_to_data(entry[0:3], min_noise_acc, max_noise_acc)
        gyro_x, gyro_y, gyro_z = add_noise_to_data(entry[3:6], min_noise_gyro, max_noise_gyro)
        new_values.append([acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z])
        timestamps.append(start_time)
        start_time += sensor_data['payload']['interval_ms']

    shift_count = random.randint(0, max_shift)
    new_values = new_values[shift_count:] + new_values[:shift_count]

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

    filename = f"{name}.artificial_data_{version}_{uuid.uuid4().hex}.cbor"

    with open(os.path.join(sub_dir, filename), 'wb') as file:
        cbor2.dump(new_sensor_data, file)

with open(readme_path, 'a') as file:
    file.write(f"\n\nNoise levels for {name}:\n")
    file.write(f"Minimum noise level for accelerometer: {min_noise_acc}\n")
    file.write(f"Maximum noise level for accelerometer: {max_noise_acc}\n")
    file.write(f"Minimum noise level for gyroscope: {min_noise_gyro}\n")
    file.write(f"Maximum noise level for gyroscope: {max_noise_gyro}\n")
    file.write(f"Max shift count: {max_shift}\n")