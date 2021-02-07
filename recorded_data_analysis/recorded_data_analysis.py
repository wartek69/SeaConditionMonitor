import json 
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import scipy.integrate as it
from scipy import signal

fifo_buffer_len = 10
dt = 0.1

def double_integrate_data(z_accels, dx_times):
	velocity = it.cumtrapz(z_accels, dx = dt)

	detrended_velocity = signal.detrend(velocity)
	location = it.cumtrapz(detrended_velocity, dx = dt)
	return [velocity,location]

def filter_accel_data(z_accels):
	fs = 10
	fc = 10  # Cut-off frequency of the filter (was 2)
	w = float(fc / (fs / 2)) # Normalize the frequency
	b, a = signal.butter(5, 0.05, 'low')
	filtered_z_axis = signal.filtfilt(b, a, z_accels)
	
	return filtered_z_axis

def moving_average(x):
    '''
    https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
        :param x: 1D numpy array containing data
        :return : moving average (floating point)
    '''
    return np.convolve(x, np.ones(len(x))/len(x), mode='valid')[0]

def get_filtered_data(recorded_data):
    filtered_data = []
    filtered_data_amount = len(recorded_data['y']) - fifo_buffer_len
    for i in range(len(recorded_data['y'])):
        if i < filtered_data_amount:
            filtered_data.append(moving_average(recorded_data['y'][i:fifo_buffer_len+i]))
    return filtered_data

def get_displacement(filtered_data):
    velocity = []
    displacement = []
    for i in range(len(filtered_data)-1):
        velocity.append((filtered_data[i] + filtered_data[i+1]) * dt)
    for i in range(len(velocity) -1):
        displacement.append((velocity[i] + velocity[i+1]) * dt)
    return velocity, displacement

if __name__ == '__main__':
    with open('recorded_data_16cm_amplitude.json') as json_file:
        recorded_data = json.load(json_file)
        #filtered_data = get_filtered_data(recorded_data)
        filtered_data = filter_accel_data(np.array(recorded_data['y']))
        displacement, velocity = get_displacement(filtered_data)
        displacement2, velocity2 = double_integrate_data(np.array(filtered_data), dt)
        plt.subplot(4, 1, 1)

        plt.plot(recorded_data['x'], recorded_data['y'])
        plt.plot(filtered_data)

        plt.subplot(4, 1, 2)
        plt.title('Displacement')

        plt.plot(np.linspace(0, len(displacement), len(displacement)), displacement)
        plt.subplot(4, 1, 3)
        plt.title('Velocity')
        plt.plot(np.linspace(0, len(velocity), len(velocity)), velocity)

        plt.subplot(4, 1, 4)
        plt.title('Displacement(cumtrapz)')
        plt.plot(np.linspace(0, len(displacement2), len(displacement2)), displacement2)

        plt.show()