import random
import numpy.random as random
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
    for i in range(self.numFloors-1):
      self.otherFloorQueues.append(0) #The floor number = list index + 2
    #States of the floor queues
    
    self.goingToFloor = 1
    
    self.scheduleERV(self.floorOneArrival, self.floor1ArrivalRate)
    self.scheduleERV(self.floorOtherArrival, self.floorXArrivalRate)
    
  def scheduleERV(self, event, propensity):
    self.events.put((self.time + random.exponential(1.0/propensity), event))
    
  def scheduleTIME(self, event, time):
    self.events.put((self.time + time, event))
    
  def elevatorCheckup(self):
    if self.currentFloorNum == 1:
      if self.firstFloorQueue > 0:
        self.scheduleTIME(lambda : self.elevatorArriveAtFloor(1), 0)
      elif self.firstFloorQueue == 0:
        maxFloor = 1
        for i in range len(self.otherFloorQueues):
          if self.otherFLoorQueues[i] > 0:
             maxFloor = i+2
          self.scheduleTIME(lambda : self.elevatorArriveAtFloor(maxFloor), self.elevatorSpeed * (maxFloor-1))
    elif self.currentFloorNum > 1:
      maxFloor = 1
        for i in range len(self.otherFloorQueues):
          if self.otherFLoorQueues[i] > 0:
             maxFloor = i+2
      distance = abs(self.currentFloorNum - maxFloor)
          self.scheduleTIME(lambda : self.elevatorArriveAtFloor(maxFloor), self.elevatorSpeed * distance)
    
    
  def floorOneArrival(self):
    self.scheduleERV(self.floorOneArrival, self.floor1ArrivalRate)
    self.firstFloorQueue += 1
  
  def floorOtherArrival(self):
    self.scheduleERV(self.floorOtherArrival, self.floorXArrivalRate)
    floor = random.randint(2,self.numFloors+1)
    if floor not in self.goingDownFloors:
      self.goingDownFloors.append(floor)
    self.otherFloorQueues[floor-2] += 1
  
  def elevatorLoad(self):
    self.scheduleTIME(self.elevatorArriveAtFloor, self.timeAtFloor + self.elevatorSpeed)
    capacityDifference = self.elevatorCapacity - self.peopleInElevator
    if self.currentFloorNum == 1:
      while self.firstFloorQueue > 0 and capacityDifference > 0:
        self.peopleInElevator += 1
        floor = random.randint(2,self.numFloors+1)
        self.goingUpFloors.append(floor)
        print(self.goingUpFloors)
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
    #IF EMPTY, do the checkup
    self.scheduleTIME(self.elevatorArriveAtFloor, self.timeAtFloor + self.elevatorSpeed)
    while self.currentFloorNum in self.goingUpFloors:
      self.peopleInElevator -= 1
      self.goingUpFloors.remove(self.currentFloorNum)
                    
  def elevatorUnloadFirst(self):
    #maybe not necessary??
    self.peopleInElevator = 0
    self.goingUp = True
    self.elevatorLoad()

  def elevatorArriveAtFloor(self):
    #ONLY calls load or unload
    self.currentFloorNum = 
    if self.goingUp:
      self.elevatorUnload()
    else:
      self.elevatorLoad()
    


  def update(self):
    next_event = self.events.get()
    self.time = next_event[0]
    next_event[1]()
        
dt = 1
sim_time = 10
snapshot_interval = 10
next_snapshot = snapshot_interval

sim = Simulation()
