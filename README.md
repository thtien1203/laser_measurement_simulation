# Laser Time-of-Flight Distance Measurement Simulation (GNU Radio)

## Description
This project simulates a pulsed laser rangefinder using GNU Radio Companion (GRC). The flowgraph generates a laser pulse, models a target at an adjustable distance using a round-trip delay and weakened echo, and add noise to the received signal. It then detects the echo and calculates the distance from its time of flight. The measured distance is displayed so it can be compared to the target distance set by the user

## Features
- Generates a laser pulse, adjusts the target distance using a slider
- Simulates a round-trip of delay and an echo that weakens with distance
- Adds Gaussian noise to the echo signal to test echo detection
- Makes the echo stand out with the other noise by FIR Filter
- Detects the echo peak with Argmax and calculate the measured distance

## Theory
distance = (c * t) / 2 where 'c' is speed of light (3 × 10⁸ m/s) and 't' is the time for light travel to the object and return. In this simulation, time is counted in samples. At a sample rate is 10 MS/s, one sample lasts 100 ns, which corresponds to 15 m of distance. The echo delay in samples is converted to distance by multiply it with c/(2*samp_rate). The distance slider and measured distance are displayed in feet (1 m = 3.28084 ft), so one sample corresponding to 15 m = 49.2426 ft. The delay calculation itself uses meter

## Key parameters
Parameter       |          Value                         |       Description
samp_rate       |     10 MS/s                            |One sample = 100 ns
speedOfLight_c  |     3 × 10⁸ m/s                        |Speed of light       
Laser pulse     |     [1]*5+[0]*995                      |Laser on for pulse 5 samples (0.5 µs) and off for 995 samples
Short period    |1000 samples (100 µs)                   |1000 samples per shot, the pulse repeats every shot
Distance slider |Min=0  Max=16,404 ft  Default=4921.26ft |The target distance set by the user
Noise amplitude |     0.02                               |To simulate real-worls noise
FIR filter      |     1,1,1,1,1                          |Matched to the first 5 samples pulse 
 
## Results
With the Gaussian noise amplitude at 0.02 and the target at default distance of 4921.26 ft, the measured distance matches the true distance. The filtered echo peak is the highest point in each shot, so Argmax finds its position correctly. When the slider is moved, the echo changes strength with distance. A target farther from the laser returns a weaker echo, and a target closer to the laser returns a stronger echo 

## Issues
The measured distance matches the true distance for targets up to about 6003.93 ft. Beyond that distance, the echo becomes so weak so that it is no longer the highest echo peak in the filtered signal. The random noise produces peaks that are as high as, or higher than the echo, so Argmax sometimes picks a noise peak and measured distance jumps to wrong values

## Solution
Reduce the noise so the Argmax can still find the echo peak when the echo is weak

## How to run
- Install GNU Radio if it is not installed (on Ubuntu):
sudo apt install gnuradio
- Download `laser_measurement.grc` to your computer
- Open the file in GNU Radio Companion, either by running this command in the folder that contains the file:
gnuradio-companion laser_measurement.grc or by starting `gnuradio-companion` and choosing File → Open
- Click Run to start the simulation.