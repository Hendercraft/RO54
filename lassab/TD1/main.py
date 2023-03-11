from math import log10
import csv

import requests


class RSSISample:

    def __init__(self, mac_address: str, rssi: list[float]) -> None:
        self.mac_address = mac_address
        self.rssi = rssi
        self.avg_rssi = self.get_average_rssi()

    def get_average_rssi(self) -> float:
        avg_mW : float
        n = 0
        for rssi in self.rssi:
            avg_mW += 10**(rssi/10.)
            n +=1
        return 10. * log10(avg_mW/n)


class FingerprintSample:
	def __init__(self, samples: list[RSSISample]) -> None:
		self.samples = samples

class SimpleLocation:
	def __init__(self, x: float, y: float, z: float) -> None:
		self.x = x
		self.y = y
		self.z = z

class Fingerprint:
	def __init__(self, position: SimpleLocation, sample: FingerprintSample) -> None:
		self.position = position
		self.sample = sample

class FingerprintDatabase:
	def __init__(self) -> None:
		self.db = []

data = requests.get("https://raw.githubusercontent.com/flassabe/TD1/master/data.csv")
data = csv.reader(data.content.decode().strip().split("\n"), delimiter=",")
data = list(data)
for row in data :
    print(row)
    #One row equals to the reading of the rssi for one coordinate at one orientation
    #Todo : Make a fingerprint for each location with a different orientation, each finger print will have fingerprintsample, and each sample will have a mac adress and a RSSI
    #parse trough all fingerprint with the same coord and create a new one with the 
    
