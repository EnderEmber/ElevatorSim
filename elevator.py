class Simulation:
  def __init__(self):
    self.numFloors = 6
    self.elevatorCapacity = 8
    self.floor1ArrivalRate = .5 #Per minute
    self.floorXArrivalRate = .1 #Per minute
    self.elevatorSpeed = 10 #seconds between floors
    self.timeAtFloor = 15 #seconds when stopped
    self.events = PriorityQueue()
    #Initialization parameters

    self.goingUpFloors = []
    self.goingDownFloors = []
    self.goingUp = True
    self.currentFloorNum = 1
    #States of the elevator

    self.firstFloorQueue = 0
    self.otherFloorQueues = []
    for i in range(numFloors-1):
      self.otherFloorQueues[i] = 0 #The floor number = list index + 2
    #States of the floor queues
  
