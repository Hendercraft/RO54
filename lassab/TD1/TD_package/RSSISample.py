from math import log10

class RSSISample:
    def __init__(self, mac_address: str) -> None:
        self.mac_address = mac_address
        self.rssi_list = []
        self.avg_rssi = 0

    def compute_average_rssi(self) -> float:
        avg_mW = 0.
        n = 0
        #Parse the list of rssi, convert the value to mW and add it to the avg
        for rssi in self.rssi_list:
            avg_mW += 10**(rssi/10.)
            n +=1
        #Divide by the number of element to have the mean value, and convert it to dB
        self.avg_rssi = 10. * log10(avg_mW/n)
    
    def add(self,rssi):
        self.rssi_list.append(rssi)