class OpenFile(object):
    def __init__(self, path):
        self.path = path
        self.GetCoordinates()

    # Method: Open text file and read contents
    def OpenFile(self):
        self.inputData = ""
        self.arrayX = []
        self.arrayY = []
        self.arrayZ = []
        self.arrayHoverTime = []

        #Open File and read contents
        myFile = open(self.path, 'r')
        self.inputData = myFile.readlines()

        # Close File
        myFile.close()

    # Method: Extract Coordinates from file contents
    def GetCoordinates(self):
        deliminator = ","
        self.OpenFile()
        
        # Read each line (co-ordinate) and assign to appropriate array
        for line in self.inputData:
            contents = line.split(deliminator)
            self.arrayX.append(float(contents[0]))
            self.arrayY.append(float(contents[1]))
            self.arrayZ.append(float(contents[2]))
            self.arrayHoverTime.append(float(contents[3]))
        
