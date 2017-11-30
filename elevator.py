import random
from queue import PriorityQueue

class Simulation:
  def __init__(self):
    self.time = 0
    self.numFloors = 6
    self.elevatorCapacity = 8
    self.floor1ArrivalRate = 1 #Per minute
    self.floorXArrivalRate = self.floor1ArrivalRate/(self.numFloors-1) + 0.01 #Per minute
    self.elevatorSpeed = 0.17 #seconds between floors
    self.timeAtFloor = 0.25 #seconds when stopped
    self.events = PriorityQueue()
    #Initialization parameters

    self.goingUpFloors = []
    self.goingDownFloors = []
    self.goingUp = True
    self.currentFloorNum = 1
    self.peopleInElevator = 0
    #States of the elevator

    self.firstFloorQueue = 0
    self.otherFloorQueues = []
    for i in range(numFloors-1):
      self.otherFloorQueues[i] = 0 #The floor number = list index + 2
    #States of the floor queues
    
    self.scheduleERV(self.floorOneArrival, self.floor1ArrivalRate)
    self.scheduleERV(self.floorOtherArrival, self.floorXArrivalRate)

  def scheduleERV(self, event, propensity):
    self.events.put((self.time + random.exponential(1.0/propensity), event))
    
  def scheduleNRV(self, event, mean, stddev):
    self.events.put((self.time + random.normal(mean, stddev), event))
    
  def scheduleTIME(self, event, time):
    self.events.put((self.time + time, event))
    
  def floorOneArrival(self):
    self.scheduleERV(self.floorOneArrival, self.floor1ArrivalRate)
    self.firstFloorQueue += 1
  
  def floorOtherArrival(self):
    self.scheduleERV(self.floorOtherArrival, self.floorXArrivalRate)
    floor = random.randint(2,self.numFloors)
    if floor not in self.goingDownFloors:
      self.goingDownFloors.append(floor)
    self.otherFloorQueues[floor-2] += 1
  
  def elevatorLoad(self):
    self.scheduleTIME(self.elevatorArriveAtFloor, .25)
    capacityDifference = self.elevatorCapacity - self.peopleInElevator
    if self.currentFloorNum == 1:
      while self.firstFloorQueue > 0 and capacityDifference > 0:
        self.peopleInElevator += 1
        floor = random.randint(2,self.numFloors)
        self.goingUpFloors.append(floor)
        self.firstFloorQueue -= 1
        capacityDifference -= 1
    else:
      floorIndex = self.currentFloorNum - 2
      while self.otherFloorQueues[floorIndex] > 0 and capacityDifference > 0:
        self.peopleInElevator += 1
        self.otherFloorQueues[floorIndex] -= 1
        capacityDifference -= 1
      if self.otherFloorQueues[floorIndex] == 0:
        self.goingDownFloors.remove(self.currentFloorNum)

  def elevatorUnload(self):
    self.scheduleTIME(self.elevatorArriveAtFloor, self.timeAtFloor + self.elevatorSpeed)
    while self.currentFloorNum in self.goingUpFloors:
      self.peopleInElevator -= 1
      self.goingUpFloors.remove(self.currentFloorNum)
                    
  def elevatorUnloadFirst(self):
    self.peopleInElevator = 0
    self.goingUp = True
    self.elevatorLoad()

  def elevatorArriveAtFloor(self):
    if self.goingUp:
      self.currentFloorNum += 1
      if self.currentFloorNum in self.goingUpFloors:
        self.elevatorUnload()
        if self.goingUpFloors == []:
          if self.currentFloorNum > max(self.goingDownFloors):
            self.goingUp = False
          elif self.currentFloorNum == max(self.goingDownFloors):
            floorIndex = self.currentFloorNum - 2
            capacityDifference = self.elevatorCapacity
            while self.otherFloorQueues[floorIndex] > 0 and capacityDifference > 0:
              self.peopleInElevator += 1
              self.otherFloorQueues[floorIndex] -= 1
              capacityDifference -= 1
            self.goingUp = False
      else:
        if self.goingUpFloors == []:
          if self.currentFloorNum == max(self.goingDownFloors):
            floorIndex = self.currentFloorNum - 2
            capacityDifference = self.elevatorCapacity
            while self.otherFloorQueues[floorIndex] > 0 and capacityDifference > 0:
              self.peopleInElevator += 1
              self.otherFloorQueues[floorIndex] -= 1
              capacityDifference -= 1
            self.goingUp = False
        self.schedule(self.elevatorArriveAtFloor, self.elevatorSpeed)
    else:
      self.currentFloorNum -= 1
      if self.currentFloorNum == 1:
        self.elevatorUnloadFirst()
      elif self.currentFloorNum in self.goingDownFloors:
        self.elevatorLoad()
