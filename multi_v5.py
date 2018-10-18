# TEAM SYMBIOSIS
# SIT302 - Project Delivery
# Trimester 2, 2018
# CrazyFlie 2.0 Drone - Flight-Control Solution Multi-waypoint Upgrade (v5)

# NOTE: This version flies multi-waypoints with time delays (set by user) at each point
#       Designed to be used in conjunction with Unity / C#

"""
Bitcraze CrazyFlie 2.0 Drone
 - Automatic Flight-Control Prototype Solution

This program connects to the Crazyflie at the `URI` and runs a multi-waypoint flight sequence.

This program does not utilise an external location system: it has been
tested with (and designed for) the Flowdeck in line with our Sprint 2 goals.

Written by:
Paul Hammond (for Symbiosis Team)
216171484

ATTENTION: 	
X, Y, Z follows standard 3-D Co-ordinate Geometry (+Y = Front, +X = Right, +Z = Up)
Positive rotation is anti-clockwise

CHANGE LOG:
from (v4): Code updated to incorporate OOP
from (v4): Single-point bug fix
"""

import FileIO              # Class
import FlightParameters    # Class
import logging
import time
import sys
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)    # investigate this for logging battery level

'''	   
GENERAL ATTRIBUTES
'''
# Constants
HOVER_HEIGHT_STD = 0.5        # metres
LAND_HEIGHT = 0.1             # metres
HOVER_TIME_STD = 1            # seconds
DESTINATION_HOVER_TIME = 15   # seconds (to be set as desired)
VELOCITY_SIDE = 0             # do not modify
URI = "radio://0/80/2M"       # CrazyRadio Frequency
OUTPUT_FILE = "C:\\Test\\Multi-waypoints\\Waypoints.txt"


'''
Methods
'''
# Method: Fly and climb / descend to next designated waypoint (x, y, z)
def Traverse(velocityFWD, travelTime, currentHeight, destinationHeight):
    # Calculate number of iterations and climb rate
    iterations = travelTime * 10
    heightDrone = currentHeight
    climbRate = (destinationHeight - currentHeight) / iterations      # +ve = ascend, -ve = descend  
    
    # Traverse Flight Path
    print("\nTraversing to height of %f" %(destinationHeight))
    for i in range(iterations):
        heightDrone += climbRate
        print("Current height: %.1f" %(heightDrone))
        cf.commander.send_hover_setpoint(velocityFWD, VELOCITY_SIDE, 0, heightDrone)
        time.sleep(0.1)


# Method: Hover Drone
def Hover(hoverHeight, hoverTime):
    # Convert time to iterations
    iterations = int(hoverTime * 10)  

    # Hover Drone
    print("\nHovering at %f metres" %(hoverHeight))
    for i in range(iterations):
        cf.commander.send_hover_setpoint(0, 0, 0, hoverHeight)
        time.sleep(0.1)


# Method: Rotates the drone anti-clockwise whilst in hover
def Rotate(rotationAngle, hoverHeight):
    YAWTIME = 3 	# seconds

    # Calculate yawRate and iterations
    yawRate = rotationAngle / YAWTIME    # degrees / second           
    iterations = YAWTIME * 10

    # Rotate Drone
    print("\nRotating to %f degrees" %(rotationAngle))
    for i in range(iterations):
        cf.commander.send_hover_setpoint(0, 0, yawRate, hoverHeight)
        time.sleep(0.1)


# Method: Run the flight sequence
def RunFlightSequence(angle, velocityForward, travelTime, hoverTime, heightCurrent, heightDestination):
    # HOVER AT WAYPOINT FOR USER-ALLOTED TIME (SEC)
    if (hoverTime != 0):
        print("Hovering at waypoint for %f seconds" %(hoverTime))
        Hover(heightCurrent, hoverTime)

    # ROTATE DRONE TOWARDS NEXT WAYPOINT
    # Rotate to correct orientation
    if (angle != 0):
        Rotate(angle, heightCurrent)
           
    # TRAVERSE TO NEXT WAYPOINT
    if (travelTime != 0):
        Traverse(velocityForward, travelTime, heightCurrent, heightDestination)




'''			
# Flight-Control Program
'''
if __name__ == '__main__':
    # Get coordinates and calculate flight parameters
    flightInputs = FileIO.OpenFile(OUTPUT_FILE)
    flightParams = FlightParameters.DefineParameters(flightInputs)

    
    #'''
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(2)

        # TAKE-OFF
        Hover(HOVER_HEIGHT_STD, HOVER_TIME_STD)
        
        # FLY TO WAY-POINTS
        index = 0
        while (index < len(flightParams.arrayDistance)):
            RunFlightSequence(flightParams.arrayRotationAngle[index], flightParams.arrayVelocityFWD[index], flightParams.arrayTravelTime[index], flightParams.arrayHoverTime[index], flightParams.arrayZ[index], flightParams.arrayZ[index + 1])
            index += 1

        # Rotate back to origin
        RunFlightSequence(flightParams.arrayRotationAngle[index], 0, 0, flightParams.arrayHoverTime[index], HOVER_HEIGHT_STD, 0)
        
        # LAND and SHUTDOWN
        Hover(LAND_HEIGHT, HOVER_TIME_STD)                       
        
        # Engine shut-off
        cf.commander.send_stop_setpoint()
    #'''
