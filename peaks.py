import cbor2
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def read_cbor_file(file_path):
    with open(file_path, 'rb') as file:
        data = cbor2.load(file)
    return data

file_path = 'TEST_TRIANGLE.5aevcvir.cbor'
sensor_data = read_cbor_file(file_path)

timestamps = []
acc_x, acc_y, acc_z = [], [], []
gyro_x, gyro_y, gyro_z = [], [], []

interval_ms = 10.0
current_timestamp = 0

for entry in sensor_data['payload']['values']:
    timestamps.append(current_timestamp)
    acc_x.append(entry[0])
    acc_y.append(entry[1])
    acc_z.append(entry[2])
    gyro_x.append(entry[3])
    gyro_y.append(entry[4])
    gyro_z.append(entry[5])
    current_timestamp += interval_ms

timestamps = [t / 1000 for t in timestamps]

def find_all_peaks(data, upper_threshold, lower_threshold):
    upper_peaks, _ = find_peaks(data, height=upper_threshold)
    lower_peaks, _ = find_peaks([-val for val in data], height=-lower_threshold)
    all_peaks = sorted(list(upper_peaks) + list(lower_peaks))
    return all_peaks

def find_matching_peaks(time, peaks1, peaks2, tolerance):
    matches = []
    for i in peaks1:
        for j in peaks2:
            if abs(time[i] - time[j]) <= tolerance:
                matches.append((time[i], time[j]))
    return matches

acc_x_peaks = find_all_peaks(acc_x, 10, -10)
acc_y_peaks = find_all_peaks(acc_y, 10, -10)
acc_z_peaks = find_all_peaks(acc_z, 10, -10)

gyro_x_peaks = find_all_peaks(gyro_x, 90, -90)
gyro_y_peaks = find_all_peaks(gyro_y, 90, -90)
gyro_z_peaks = find_all_peaks(gyro_z, 90, -90)

tolerance = 0.1  # 100 ms tolerance
print("Matching Peaks within 100 ms tolerance:")

# X-axis matching peaks
matching_x = find_matching_peaks(timestamps, acc_x_peaks, gyro_x_peaks, tolerance)
print("\nAcc X and Gyro X matching peaks:")
for match in matching_x:
    print(f"  Acc X Peak Time: {match[0]:.2f} s, Gyro X Peak Time: {match[1]:.2f} s")

# Y-axis matching peaks
matching_y = find_matching_peaks(timestamps, acc_y_peaks, gyro_y_peaks, tolerance)
print("\nAcc Y and Gyro Y matching peaks:")
for match in matching_y:
    print(f"  Acc Y Peak Time: {match[0]:.2f} s, Gyro Y Peak Time: {match[1]:.2f} s")

# Z-axis matching peaks
matching_z = find_matching_peaks(timestamps, acc_z_peaks, gyro_z_peaks, tolerance)
print("\nAcc Z and Gyro Z matching peaks:")
for match in matching_z:
    print(f"  Acc Z Peak Time: {match[0]:.2f} s, Gyro Z Peak Time: {match[1]:.2f} s")

def plot_with_selected_peaks(time, data, label, color, peaks):
    plt.plot(time, data, label=label, alpha=0.7, color=color)
    plt.plot([time[i] for i in peaks], [data[i] for i in peaks], "x", color=color, label=f"{label} Peaks")

plt.figure(figsize=(10, 6))
plot_with_selected_peaks(timestamps, acc_x, 'Acc X', 'blue', acc_x_peaks)
plot_with_selected_peaks(timestamps, acc_y, 'Acc Y', 'orange', acc_y_peaks)
plot_with_selected_peaks(timestamps, acc_z, 'Acc Z', 'green', acc_z_peaks)
plt.xlabel("Time (s)")
plt.ylabel("Accelerometer (m/s²)")
plt.title("Accelerometer Data with Peaks")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plot_with_selected_peaks(timestamps, gyro_x, 'Gyro X', 'purple', gyro_x_peaks)
plot_with_selected_peaks(timestamps, gyro_y, 'Gyro Y', 'brown', gyro_y_peaks)
plot_with_selected_peaks(timestamps, gyro_z, 'Gyro Z', 'red', gyro_z_peaks)
plt.xlabel("Time (s)")
plt.ylabel("Gyroscope (°/s)")
plt.title("Gyroscope Data with Peaks")
plt.legend()
plt.grid(True)
plt.show()
