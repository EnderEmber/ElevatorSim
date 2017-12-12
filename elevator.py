import random
import numpy.random as random
from queue import PriorityQueue

class Simulation:
  def __init__(self):
    self.time = 0
    self.numFloors = 50
    self.elevatorCapacity = 25
    self.floor1ArrivalRate = 1 #Per minute
    self.floorXArrivalRate = self.floor1ArrivalRate/(self.numFloors) - 0.01 #Per minute
    self.elevatorSpeed = 0.17 #seconds between floors
    self.timeAtFloor = 0.25 #seconds when stopped
    self.events = PriorityQueue()
    #Initialization parameters

    self.goingUpFloors = []     #list of floors elevator is going to on the way up
    self.goingDownFloors = []   #list of floors with people waiting to go down 
    self.currentFloorNum = 1
    self.peopleInElevator = 0
    #States of the elevator

    self.firstFloorQueue = 0    #how many people are waiting on the first floor
    self.otherFloorQueues = []  #how many people are waiting on the other floors
    for i in range(self.numFloors-1):
      self.otherFloorQueues.append(0) #The floor number = list index + 2
    #States of the floor queues
    
    self.goingToFloor = 1       #destination
        
    self.scheduleERV(self.floorOneArrival, self.floor1ArrivalRate)
    self.scheduleERV(self.floorOtherArrival, self.floorXArrivalRate)
    self.scheduleTIME(self.elevatorCheckup, 5)
    
  def scheduleERV(self, event, propensity):
    self.events.put((self.time + random.exponential(1.0/propensity), event))
    
  def scheduleTIME(self, event, period):
    self.events.put((self.time + period + 0.001, event))
    
  def elevatorCheckup(self):
    """This function is called when the elevator is empty to check where the 
    elevator is and where it needs to go next"""
    if self.currentFloorNum == 1:
      if self.firstFloorQueue > 0:
        self.goingToFloor = 1
        self.scheduleTIME(self.elevatorArriveAtFloor, 0)
      elif self.firstFloorQueue == 0:
        self.goingToFloor = 1
        for i in range(len(self.otherFloorQueues)):
          if self.otherFloorQueues[i] > 0:
            self.goingToFloor = i+2
        self.scheduleTIME(self.elevatorArriveAtFloor, (self.elevatorSpeed * (self.goingToFloor-1)))
    else:
      self.goingToFloor = 1
      for i in range(len(self.otherFloorQueues)):
        if self.otherFloorQueues[i] > 0:
          self.goingToFloor = i+2
      distance = abs(self.currentFloorNum - self.goingToFloor)
      self.scheduleTIME(self.elevatorArriveAtFloor, (self.elevatorSpeed * distance))
    
    
  def floorOneArrival(self):
    """This function adds one person to the first floor queue and schedules the 
    next person arriving at the floor"""
    self.scheduleERV(self.floorOneArrival, self.floor1ArrivalRate)
    self.firstFloorQueue += 1
  
  def floorOtherArrival(self):
    """This function adds one person to a floor queue that is not the first 
    floor, adds the floor number to the going down list, and schedules the next
    person arriving at a floor"""
    self.scheduleERV(self.floorOtherArrival, self.floorXArrivalRate)
    floor = random.randint(2,self.numFloors+1)
    if floor not in self.goingDownFloors:
      self.goingDownFloors.append(floor)
    self.otherFloorQueues[floor-2] += 1
  
  def elevatorLoad(self):
    """This function loads people into the elevator as long as there is space 
    in the elevator and people waiting to get on. The function is split for 
    whether or not the elevator is at the first floor so that people getting on
    the elevator at the first floor can be assigned destination floors and 
    those floor numbers added to the going up floors list"""
    if self.currentFloorNum == 1:
      capacityDifference = self.elevatorCapacity - self.peopleInElevator
      while self.firstFloorQueue > 0 and capacityDifference > 0:
        self.peopleInElevator += 1
        floor = random.randint(2,self.numFloors+1)
        self.goingUpFloors.append(floor)
        self.firstFloorQueue -= 1
        capacityDifference -= 1
      if self.goingUpFloors == []:
        if self.goingDownFloors != []:
          self.goingToFloor = max(self.goingDownFloors)
          distance = self.goingToFloor - 1
          self.scheduleTIME(self.elevatorArriveAtFloor, (self.timeAtFloor + (self.elevatorSpeed * distance)))
        else:
          self.scheduleTIME(self.elevatorCheckup, 5)
      else:
        self.goingToFloor = min(self.goingUpFloors)
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
        self.goingDownFloors.remove(self.currentFloorNum)
      self.goingToFloor = 1
      for item in self.goingDownFloors:
        if item > self.goingToFloor and item < self.currentFloorNum:
          self.goingToFloor = item
      distance = abs(self.goingToFloor - self.currentFloorNum)
      self.scheduleTIME(self.elevatorArriveAtFloor, (self.timeAtFloor + (self.elevatorSpeed * distance)))

  def elevatorUnload(self):
    """This function unloads the elevator at all floors that are not the first.
    If the current floor is in the going up floors list, it removes a person 
    from the elevator and the floor number from the list until there is no one 
    else  wanting to get off at that floor then goes to the next floor from the
    list. Once the elevator is completely unloaded it calls the checkup function"""
    while self.currentFloorNum in self.goingUpFloors:
      self.peopleInElevator -= 1
      self.goingUpFloors.remove(self.currentFloorNum)
    if self.peopleInElevator == 0:
      self.scheduleTIME(self.elevatorCheckup, 0)
    else:
      self.goingToFloor = min(self.goingUpFloors)
      distance = abs(self.goingToFloor - self.currentFloorNum)
      self.scheduleTIME(self.elevatorArriveAtFloor, (self.timeAtFloor + (self.elevatorSpeed * distance)))
                    
  def elevatorUnloadFirst(self):
    """This function unloads the elevator completely at the first floor then 
    schedules the checkup function"""
    self.peopleInElevator = 0
    self.scheduleTIME(self.elevatorCheckup, 0)

  def elevatorArriveAtFloor(self):
    """This function is called wheen the elevator arrives at a floor and calls 
    either the load or unload function depending on if the elevator is 
    travelling up (unload) or down (load)"""
    self.currentFloorNum = self.goingToFloor
    if self.currentFloorNum == 1:
      if self.peopleInElevator > 0:
        self.scheduleTIME(self.elevatorUnloadFirst, 0)
      else:
        self.scheduleTIME(self.elevatorLoad, 0)
    elif self.goingUpFloors != []:
      self.scheduleTIME(self.elevatorUnload, 0)
    else:
      self.scheduleTIME(self.elevatorLoad, 0)
    
  def update(self):
    """This function updates the simulation"""
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
  if ( sim.time > next_snapshot):
    print("Elevator state\n at time", int(sim.time))
    print("   ___")
    for i in range(sim.numFloors, 1, -1):
      floorString = str(i) + " "
      if i < 10:
        floorString += " "
      if i == sim.currentFloorNum:
        floorString += "[" +str(sim.peopleInElevator) + "] "
      else:
        floorString += " |  "
      floorQueue = sim.otherFloorQueues[i-2]

      for j in range(floorQueue):
        floorString += "o "
      print(floorString)
    firstFloorString = "1 "
    if sim.currentFloorNum == 1:
      firstFloorString += " [" +str(sim.peopleInElevator) + "] "
    else:
      firstFloorString += "  |  "
    for k in range(sim.firstFloorQueue):
      firstFloorString += "o "
    print(firstFloorString)
    print("   ___\n")
    """  
    print("Time: ", sim.time, "\n People in Elevator:", sim.peopleInElevator, "\n Floor Queues: \n Floor 1:", sim.firstFloorQueue)
    for i in range(len(sim.otherFloorQueues)):
      print("Floor " + str(i+2) + ":", sim.otherFloorQueues[i])
    """
    next_snapshot += snapshot_interval
