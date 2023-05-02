import csv
from TD_package.Fingerprint import Fingerprint
from TD_package.SimpleLocation import SimpleLocation

class FingerprintDatabase:
    def __init__(self) -> None:
        self.db = []

    def match_location(self,location) -> Fingerprint:
        """
		Parse the db and return the fingerprint with the matching location
        If there is no match, create an new fingerprint and add it to the db before returning it
		"""
        for fingerprint_parser in self.db :
            if fingerprint_parser.position == location:
                return fingerprint_parser
        # if we didn't find any match

        #Create an new fingerprint
        fingerprint = Fingerprint(location)
        self.db.append(fingerprint)
        return fingerprint

    def compute_avg_all(self):
        for fingerprint_Parser in self.db:
            for sample in fingerprint_Parser.samples:
                sample.get_average_rssi()
        

    def read_csv(self, file_path: str) -> None:
        # open the csv file
        with open(file_path, newline='') as csv_file:
            # create a csv reader object
            csv_reader = csv.reader(csv_file, delimiter=',')
          
            # iterate over the rows of the csv file
            for row in csv_reader:
                # get the coordinates and orientation
                x, y, z, orientation = map(float, row[:4])
                # create a SimpleLocation object
                location = SimpleLocation(x, y, z)

                # Parse the existing database looking for a location match
                # If we don't find a match, the function create a new fingerprint for us
                fingerprint = self.match_location(location)

                #Add the remaning rssi value and mac_adress of the line to the fingerprint
                for i in range(4, len(row), 2):
                    mac_address = row[i]
                    rssi = float(row[i+1])
                    # add them to the existing fingerpring
                    fingerprint.add(rssi,mac_address)
                


    def to_csv_bis(self, filename: str) -> None:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # write data rows
            for fingerprint in self.db:
                row = [fingerprint.position.x, fingerprint.position.y, fingerprint.position.z,0]
                for sample in fingerprint.samples:
                   row.append(sample.mac_address)
                   row.append(sample.avg_rssi)
                writer.writerow(row)