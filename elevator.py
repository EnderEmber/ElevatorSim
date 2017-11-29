import random

class Simulation:
  def __init__(self):
    self.numFloors = 6
    self.elevatorCapacity = 8
    self.floor1ArrivalRate = .5 #Per minute
    self.floorXArrivalRate = self.floor1ArrivalRate/(self.numFloors-1) + 0.01 #Per minute
    self.elevatorSpeed = 10 #seconds between floors
    self.timeAtFloor = 15 #seconds when stopped
    self.events = PriorityQueue()
    self.randomPeopleWeighted = [1,1,1,1,2,2,2,3,3,4] # most of the time only one or two people will arrive at the elevator, 
                                                      # or one person with luggage, but sometimes more people with more 
                                                      # luggage will arrive.
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
  
  def floorOneArrival(self):
    newPeople = random.choice(self.randomPeopleWeighted)
    self.firstFloorQueue += newPeople
    for i in range newPeople:
      self.goingUpFloors.append(random.randint(2,self.numFloors))
  
  def floorOtherArrival(self):
    floor = random.randint(2,self.numFloors)
    newPeople = random.choice(self.randomPeopleWeighted)
    self.goingDownFloors.append(floor)
    self.otherFloorQueues[floor-2] += newPeople
  
  def elevatorLoad(self):
    capacityDifference = self.elevatorCapacity - self.peopleInElevator
    if self.currentFloorNum = 1:
      while self.firstFloorQueue > 0 and capacityDifference > 0:
        self.peopleInElevator += 1
        self.firstFloorQueue -= 1
        capacityDifference -= 1
    else:
      floorIndex = self.currentFloorNum - 2
      while self.otherFloorQueues[floorIndex] > 0 and capacityDifference > 0:
        self.peopleInElevator += 1
        self.otherFloorQueues[floorIndex] -= 1
        capacityDifference -= 1
