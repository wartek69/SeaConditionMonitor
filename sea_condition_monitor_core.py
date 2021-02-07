import logging
from mpu6050 import mpu6050
import time
from collections import deque
import asyncio
import numpy as np
import signal 
import json
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
dt = 0.1
fifo_length = 10

class SeaConditionMonitorCore:
    def __init__(self):
        self.z_calibration_value = None
        self.z_velocity_buffer = deque([], maxlen=fifo_length)
        self.z_calibrated_accelerations = deque([], maxlen=fifo_length)
        self.z_displacement = 0
        self.z_velocity = 0
        self.sensor = mpu6050(0x68)
        range = self.sensor.read_accel_range()
        logging.info('Accel range: ' + str(range))

        self.get_test_data()
        self.calibrate_sensor()


        self.loop = asyncio.get_event_loop()
        self.loop.call_soon(self.get_measurements)

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()

    
    def calibrate_sensor(self):
        '''
            Gets the z acceleration while being stationary
        '''
        calibration_values = []
        for i in range(10):
            calibration_values.append(self.sensor.get_accel_data()['z'])
            time.sleep(dt)

        self.z_calibration_value = self.moving_average(calibration_values)
        self.z_calibrated_accelerations = deque([], maxlen=fifo_length)
        self.z_velocity_buffer = deque([], maxlen=fifo_length)
        self.z_displacement = 0
        self.z_velocity = 0

    def get_measurements(self):
        if self.z_calibration_value is not None:
            self.z_calibrated_accelerations.append(self.sensor.get_accel_data()['z'] -  self.z_calibration_value)
            if(len(self.z_calibrated_accelerations) == fifo_length):
                z_ma_acceleration = self.moving_average(self.z_calibrated_accelerations)
                self.z_velocity_buffer.append(z_ma_acceleration * dt)
                if(len(self.z_velocity_buffer) == fifo_length):
                    #z_ma_velocity = self.moving_average(self.z_velocity_buffer)
                    #TODO velocity calculations is a mistake, should be a buffer two accelertions -> 1 velocity
                    self.z_velocity += z_ma_acceleration * dt 
                    self.z_displacement += self.z_velocity * dt
                    logging.info(f'''
                        z calibrated accelerations: {self.z_calibrated_accelerations[0]}
                        z acceleration (ma): {z_ma_acceleration} 
                        z velocity (ma): {self.z_velocity} 
                        z displacement: {self.z_displacement}''')
        else:
            logging.warning('Sensor not calibrated yet, please calibrate the sensor first!')

        self.loop.call_later(dt, self.get_measurements)

    def moving_average(self, x):
        '''
        https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
         :param x: 1D numpy array containing data
         :return : moving average (floating point)
        '''
        return np.convolve(x, np.ones(len(x))/len(x), mode='valid')[0]
    
    def get_test_data(self):
        self.calibrate_sensor()
        input('press enter to start measurements')
        x = []
        y = []
        for i in range(100):
            x.append(i)
            acc = self.sensor.get_accel_data()['z'] -  self.z_calibration_value
            y.append(acc)
            time.sleep(0.1)
        data = {'x': x, 'y': y}
        with open('recorded_data.json', 'w') as outfile:
            json.dump(data, outfile)

    def exit_gracefully(self, signum, frame):
        self.loop.stop()
        self.close(True)

if __name__ == '__main__':
    sea_condition_monitor_core = SeaConditionMonitorCore()