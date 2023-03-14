from math import sqrt, pow
import numpy as np
class Position:
    def __init__(self, coords: list):
        self.coords = coords

class Emettor(Position):
    def __init__(self, coords: list, distance : float):
        super().__init__(coords)
        self.distance = distance

    def compute_distance(self,coords:list) -> float:
        dis = 0
        for i in range(0,3):
            dis += pow(self.coords[i] - coords[i],2)
        return sqrt(dis)

class Terminal(Position):
    def __init__(self, coords: list):
        super().__init__(coords)


class Locator:
    def __init__(self, emettors: list[Emettor]):
        self.emettors = emettors
        self.min = [999,999,999]
        self.max = [-999,-999,-999]

    def compute_search_area(self):
        for i in self.emettors:
            for j in range(0,3):
                if i.coords[j] < self.min[j]:
                    self.min[j] = i.coords[j]
                elif i.coords[j] > self.max[j]:
                    self.max[j] = i.coords[j]
    
    def compute_terminal(self,step : float) -> Terminal:
        dist_min = 9999
        Estimator = None
        for i in np.arange (self.min[0],self.max[0],step):
            for j in np.arange (self.min[1],self.max[1],step):
                for k in np.arange (self.min[2],self.max[2],step):
                    distance = 0
                    for emettor in self.emettors:
                        distance += abs(emettor.compute_distance([i,j,k]) - emettor.distance)
                    if dist_min > distance:
                        dist_min = distance
                        Estimator = Terminal([i,j,k])
                        print("New best point :")
                        print(i,j,k)
                        print("distance :", distance)
        return Estimator

ap1 = Emettor((0.5,0.5,0.5),3)
ap2 = Emettor((4,0,0),2)
ap3 = Emettor((4,5,5),4.2)
ap4 = Emettor((3,3,3),2.5)

locator = Locator((ap1,ap2,ap3,ap4))
locator.compute_search_area()
locator.compute_terminal(0.1)
print(locator.compute_terminal(0.1).coords)
