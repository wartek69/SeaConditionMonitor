# SeaConditionMonitor
A rpi based sea (wave) monitoring tool

## TODO
- reset the integration after each period to minimise error accumulation 
- Add a webinterface to show the z translation and reset the measurements (socketio)
- Constantly get the min/max of the translation measurements and show them in the webinterface
- Calculate significant wave height using the formula (4*std)

## Data
All the data was recorded by manually moving the GY-521 accelerometer up and down near a measurement pole of 32 cm.
