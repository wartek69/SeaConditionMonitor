# SeaConditionMonitor
A rpi based sea (wave) monitoring tool

##TODO
- Connect imu sensor to rpi
- Write basic code to interface with the imu and get measurements
- Write code to init measurements to 0 and measure z translation
- Add a webinterface to show the z translation and reset the measurements (socketio)
- Constantly get the min/max of the translation measurements and show them in the webinterface
- Calculate significant wave height using the formula (4*std)

##Improvements
- Instead of manually reseting the translation counter, reset it on each 0 acceleration passing. This will keep the integration error in bounds. In waves we normally will hit the 0m/s^2 acceleration only in the maxima/minima of the wave and thus we can always calculate the maxima/minima for each wave period -> need experimenting to confirm this theory

- If these results will not give stable results per period we can always store multiple max/min measurements per period and use a moving average filter to obtain more stable results
