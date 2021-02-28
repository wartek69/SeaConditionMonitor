import json 
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from numpy.linalg.linalg import det
import scipy.integrate as it
from scipy import signal

fifo_buffer_len = 15
dt = 0.1

def double_integrate_data(z_accels):
	'''
		Detrending seems to be important to limit the noise and get good results
	'''
	#z_accels = signal.detrend(z_accels)
	velocity = it.cumtrapz(z_accels, dx = dt)

	detrended_velocity = signal.detrend(velocity)
	location = it.cumtrapz(detrended_velocity, dx = dt)
	location = signal.detrend(location)

	return [velocity, location]

def filter_accel_data(z_accels):
	fs = 10
	fc = 0.5  # Cut-off frequency of the filter (was 2)
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

def get_zero_crossings(filtered_z_axis):
	a = np.array(filtered_z_axis)
	zero_crossings = np.where(np.diff(np.signbit(a)))[0]
	return zero_crossings	

if __name__ == '__main__':
    with open('recorded_data_16cm_amplitude.json') as json_file:
        recorded_data = json.load(json_file)
        #recorded_data['y'] = recorded_data['y'][:100]
        #recorded_data['x'] = recorded_data['x'][:100]
        filtered_data = get_filtered_data(recorded_data)

        #filtered_data = filter_accel_data(np.array(recorded_data['y']))
        zero_crossings = get_zero_crossings(filtered_data)
        velocity2, displacement2 = double_integrate_data(np.array(filtered_data))
        plt.figure(0)
        plt.plot(recorded_data['x'], recorded_data['y'])
        plt.plot(filtered_data)
        plt.scatter(zero_crossings, np.zeros(len(zero_crossings)), c='r')

        plt.figure(1)
        plt.title('Displacement(cumtrapz)')
        plt.plot(np.linspace(0, len(displacement2), len(displacement2)), displacement2)
        plt.scatter(zero_crossings, displacement2[zero_crossings], c='r')
        plt.show()