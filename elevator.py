import random
import numpy.random as random
from queue import PriorityQueue

class Simulation:
  def __init__(self):
    self.time = 0
    self.numFloors = 10
    self.elevatorCapacity = 10
    self.floor1ArrivalRate = 1 #Per minute
    self.floorXArrivalRate = self.floor1ArrivalRate/(self.numFloors-1) + 0.01 #Per minute
    self.elevatorSpeed = 0.17 #seconds between floors
    self.timeAtFloor = 0.25 #seconds when stopped
    self.events = PriorityQueue()
    #Initialization parameters

    self.goingUpFloors = []
    self.goingDownFloors = []
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
    self.scheduleTIME(self.elevatorCheckup, 5)
    
  def scheduleERV(self, event, propensity):
    self.events.put((self.time + random.exponential(1.0/propensity), event))
    
  def scheduleTIME(self, event, period):
    self.events.put((self.time + period + 0.001, event))
    
  def elevatorCheckup(self):
    if self.currentFloorNum == 1:
      print("We are at the first floor calling the checkup function")
      if self.firstFloorQueue > 0:
        self.goingToFloor = 1
        self.scheduleTIME(self.elevatorArriveAtFloor, 0)
      elif self.firstFloorQueue == 0:
        self.goingToFloor = 1
        for i in range(len(self.otherFloorQueues)):
          if self.otherFloorQueues[i] > 0:
            self.goingToFloor = i+2
            print("Elevator emptied, other floors:", self.otherFloorQueues)
            print("We are going to floor", self.goingToFloor)
        self.scheduleTIME(self.elevatorArriveAtFloor, (self.elevatorSpeed * (self.goingToFloor-1)))
    else:
      self.goingToFloor = 1
      for i in range(len(self.otherFloorQueues)):
        if self.otherFloorQueues[i] > 0:
          print("Floor", i+2, "has", self.otherFloorQueues[i], "people waiting")
          self.goingToFloor = i+2
      distance = abs(self.currentFloorNum - self.goingToFloor)
      print("distance to floor:", distance)
      self.scheduleTIME(self.elevatorArriveAtFloor, (self.elevatorSpeed * distance))
    
    
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
    if self.currentFloorNum == 1:
      capacityDifference = self.elevatorCapacity - self.peopleInElevator
      while self.firstFloorQueue > 0 and capacityDifference > 0:
        self.peopleInElevator += 1
        floor = random.randint(2,self.numFloors+1)
        self.goingUpFloors.append(floor)
        print(self.goingUpFloors)
        self.firstFloorQueue -= 1
        capacityDifference -= 1
      if self.goingUpFloors == []:
        print("Going Up Floors is empty")
        if self.goingDownFloors != []:
          print("Going Down Floors is not empty")
          self.goingToFloor = max(self.goingDownFloors)
          distance = self.goingToFloor - 1
          self.scheduleTIME(self.elevatorArriveAtFloor, (self.timeAtFloor + (self.elevatorSpeed * distance)))
        else:
          print("Going down floors is empty, checking up 5 minutes from now")
          self.scheduleTIME(self.elevatorCheckup, 5)
      else:
        self.goingToFloor = min(self.goingUpFloors)
        print("Minimum floor:", self.goingToFloor)
        distance = self.goingToFloor - 1
        self.scheduleTIME(self.elevatorArriveAtFloor, (self.timeAtFloor + (self.elevatorSpeed * distance)))
    else:
      capacityDifference = self.elevatorCapacity - self.peopleInElevator
      floorIndex = self.currentFloorNum - 2
      while self.otherFloorQueues[floorIndex] > 0 and capacityDifference > 0:
        self.peopleInElevator += 1
        self.otherFloorQueues[floorIndex] -= 1
        capacityDifference -= 1
      if self.otherFloorQueues[floorIndex] == 0:
        print(floorIndex, self.currentFloorNum, "The floor we're trying to remove from the list (index, floor)")
        print(self.goingDownFloors)
        self.goingDownFloors.remove(self.currentFloorNum)
      self.goingToFloor = 1
      for item in self.goingDownFloors:
        if item > self.goingToFloor and item < self.currentFloorNum:
          self.goingToFloor = item
      distance = abs(self.goingToFloor - self.currentFloorNum)
      print("Finished loading elevator going down, now going to floor", self.goingToFloor)
      self.scheduleTIME(self.elevatorArriveAtFloor, (self.timeAtFloor + (self.elevatorSpeed * distance)))
    print("Done Loading Elevator")

  def elevatorUnload(self):
    #IF EMPTY, do the checkup
    while self.currentFloorNum in self.goingUpFloors:
      print("Current floor:", self.currentFloorNum)
      print("GoingUpFloors:", self.goingUpFloors)
      print("People In Elevator:", self.peopleInElevator)
      self.peopleInElevator -= 1
      self.goingUpFloors.remove(self.currentFloorNum)
    if self.peopleInElevator == 0:
      print("elevator is empty at floor", self.currentFloorNum)
      self.scheduleTIME(self.elevatorCheckup, 0)
    else:
      self.goingToFloor = min(self.goingUpFloors)
      distance = abs(self.goingToFloor - self.currentFloorNum)
      self.scheduleTIME(self.elevatorArriveAtFloor, (self.timeAtFloor + (self.elevatorSpeed * distance)))
                    
  def elevatorUnloadFirst(self):
    self.peopleInElevator = 0
    self.scheduleTIME(self.elevatorCheckup, 0)

  def elevatorArriveAtFloor(self):
    #ONLY calls load or unload
    self.currentFloorNum = self.goingToFloor
    if self.currentFloorNum == 1:
      if self.peopleInElevator > 0:
        self.scheduleTIME(self.elevatorUnloadFirst, 0)
      else:
        self.scheduleTIME(self.elevatorLoad, 0)
    elif self.goingUpFloors != []:
      print("Elevator going up, unloading")
      self.scheduleTIME(self.elevatorUnload, 0)
    else:
      print("Elevator going down, loading")
      self.scheduleTIME(self.elevatorLoad, 0)
    
  def update(self):
    next_event = self.events.get()
    self.time = next_event[0]
    next_event[1]()
        
dt = 1
sim_time = 600
snapshot_interval = 10
next_snapshot = snapshot_interval

sim = Simulation()

while sim.time < sim_time:
  # randomly determine whether an event happens this second
    sim.update()
