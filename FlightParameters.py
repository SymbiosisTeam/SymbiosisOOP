import math

class DefineParameters(object):

    ''' Custom Constructor '''
    def __init__(self, flightInputs):
        self.flightInputs = flightInputs
        self.arrayOrientation = []        # Orientation based on 360 degree bearings (eg. 0/360, 90, 180, 270)
        self.arrayRotationAngle = []      # Rotation angle for drone to face next point
        self.arrayVelocityFWD = []
        self.arrayTravelTime = []
        self.arrayDistance = []
        self.arrayHeightDifference = []   # Vertical change between two points
        self.INIT_VELOCITY_FWD = 0.5
        self.CalculateFlightParameters()
        self.DisplayFlightParameters()
        self.arrayZ = flightInputs.arrayZ
        self.arrayHoverTime = flightInputs.arrayHoverTime
        
    
    ''' Method: Calculate Hypotenuse (using Pythagoras Theorem) and return value '''
    def Hypotenuse(self, opposite, adjacent):
        return math.sqrt((opposite * opposite + adjacent * adjacent))

    ''' Method: Calculate and return travel time as an integer value '''
    def CalculateTravelTime(self, distance):
        return abs((round)(distance / self.INIT_VELOCITY_FWD))

    ''' Method: Calculate and return drone velocity to accomodate for time as an integer '''
    def CalculateForwardVelocity(self, distance, travelTime):
        zeroValue = False
        velocity = 0
    
        if (travelTime == 0):
            velocity = 0
        else:
            velocity = distance / travelTime

        return velocity
    
    ''' Method: Calculates and returns the drone orientation according to 360 degree bearings (navigation) '''
    def CalculateOrientation(self, x, y, currentOrientation):
        angle = 0.0
        orientation = 0

        # Orientation does not change if both X and Y are 0
        if (x == 0 and y == 0):
            orientation = currentOrientation
        # Calculate orientation if flight path lies parallel to x or y axis (ie delta x or y = 0)
        elif (x == 0):
            if (y > 0):
                orientation = 0
            else:
                orientation = 180
        elif (y == 0):
            if (x > 0):
                orientation = 90
            else:
                orientation = 270
        # Calculate orientation if flight path does not lie parallel to x or y axis
        else:
            if (x < 0 and y > 0):
                angle = abs(math.degrees(math.atan(x / y)))
            else:
                angle = abs(math.degrees(math.atan(y / x)))
    
            # Calculate orientation according to line gradients
            if (x < 0 and y > 0):
                orientation = 360 - int(angle)
            elif (x > 0 and y > 0):
                orientation = int(angle)
            elif (x > 0 and y < 0):
                orientation = 90 + int(angle)
            elif (x < 0 and y < 0):
                orientation = 270 - int(angle)

        return orientation

    ''' Method: Calculates and returns the drone's angle to rotate to next waypoint '''
    def CalculateRotationAngle(self, orientation_current, orientation_destination):
        rotationAngle = 0.0
    
        # Calculate Angle
        rotationAngle = orientation_destination - orientation_current

        # Adjust Angle to account for 360 / 0 degree error
        if (rotationAngle > 180):
            rotationAngle += -360
        elif (rotationAngle < -180):
            rotationAngle += 360
        
        return rotationAngle

    ''' Method: Calculate all of the flight parameters and store in arrays '''
    def CalculateFlightParameters(self):
        index = 0
        orientation = 0

        # Append Start Orientation (Bearing: 0 degrees)
        self.arrayOrientation.append(0)
    
        while (index < len(self.flightInputs.arrayX) - 1):
            X = self.flightInputs.arrayX[index + 1] - self.flightInputs.arrayX[index]
            Y = self.flightInputs.arrayY[index + 1] - self.flightInputs.arrayY[index]
            Z_Delta = self.flightInputs.arrayZ[index + 1] - self.flightInputs.arrayZ[index]

            # Calculate and assign height changes across points
            self.arrayHeightDifference.append(Z_Delta)
        
            # Calculate and assign flight distances between points
            self.arrayDistance.append(self.Hypotenuse(X, Y))

            # Calculate horizontal and / or vertical travel times
            if (self.arrayDistance[index] != 0):
                # Calculate and assign travel times between points
                self.arrayTravelTime.append(self.CalculateTravelTime(self.arrayDistance[index]))
            else:
                # Calculate and assign vertical travel time
                self.arrayTravelTime.append(self.CalculateTravelTime(self.arrayHeightDifference[index]))
            
            # Calculate and assign forward velocities between points
            self.arrayVelocityFWD.append(self.CalculateForwardVelocity(self.arrayDistance[index], self.arrayTravelTime[index]))
       
            # Calcualte and append orientation between points
            self.arrayOrientation.append(self.CalculateOrientation(X, Y, self.arrayOrientation[index]))                 
        
            index += 1

        # Append End Orientation (Bearing: 0 degrees)
        self.arrayOrientation.append(0)

        # Calculate and assign drone rotation angles
        index = 0
        while (index < len(self.arrayOrientation) - 1):
            self.arrayRotationAngle.append(self.CalculateRotationAngle(self.arrayOrientation[index], self.arrayOrientation[index + 1]))
            index += 1

    ''' Method: Display flight parameters on console '''
    def DisplayFlightParameters(self):
        index = 0

        print("\nDisplaying flight parameters...\n")
        print("Point \t\tX-Coordinate \tY-Coordinate \tZ-Coordinate \tHover Time (sec)")

        # Traverse through each array and display co-ordinate values
        while (index < len(self.flightInputs.arrayX)):
            print("%d: \t\t%.1f \t\t%.1f \t\t%.1f \t\t%.1f" %(index, self.flightInputs.arrayX[index], self.flightInputs.arrayY[index], self.flightInputs.arrayZ[index], self.flightInputs.arrayHoverTime[index]))
            index += 1

        print("\nDistances...")
        for distance in self.arrayDistance:
            print(distance)

        print("\nTravel Times...")
        for travelTime in self.arrayTravelTime:
            print(travelTime)

        print("\nForward Velocities...")
        for velocity in self.arrayVelocityFWD:
            print(velocity)

        print("\nHeight Differences...")
        for height in self.arrayHeightDifference:
            print("%.1f" %(height))

        print("\nOrientations...")
        for bearing in self.arrayOrientation:
            print(bearing)

        print("\nAngles...")
        for angle in self.arrayRotationAngle:
            print(angle)

        print("\nWaypoint Hover Times...")
        for hoverTime in self.flightInputs.arrayHoverTime:
            print(hoverTime)
