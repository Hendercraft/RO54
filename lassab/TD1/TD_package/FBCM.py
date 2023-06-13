import numpy as np
from math import pi, log10, log
from .SimpleLocation import SimpleLocation
from .AccessPoint import AccessPoint
from .RSSISample import RSSISample
from scipy.optimize import least_squares


class FBCM:

    def __init__(self, APs: list, calibration_list) -> None:
        """Constructor
            AP_list : list of AP
            calibration_list : list of fingerprint of TD1 used to calibrate
        Return an instance of FBCM, using the AP_list and calibration data
        """
        self.APs = APs
        # list of fingerprint (used only for calibration)
        self.fbcm_index = []
        # Parsing the AP_list
        for AP in self.APs:

            # temporary list of indexes
            AP_fbcm_index = []

            # run through the fingerprint list
            for finger in calibration_list:

                # evaluate the real distance between the fingerprint and the AP
                distance = SimpleLocation.evaluateDistance(finger.position, AP.location)

                # run through the RSSI Sample list
                for sample in finger.samples:

                    # look for RSSI Samples that concern the AP (corresponding mac address)
                    if sample.mac_address == AP.mac_address:
                        # compute index with this sample distance.
                        # We filter when value are too high
                        if sample.avg_rssi > -80:
                            AP_POS_fbcm_index = self.compute_FBCM_index(distance, sample, AP)
                            break

                # adding index to the list
                # I choose to filter indexes between 3 and 3.5
                print(AP_POS_fbcm_index)
                if 2 < AP_POS_fbcm_index < 3.5:
                    AP_fbcm_index.append(AP_POS_fbcm_index)

            # averaging indexes
            self.fbcm_index.append(sum(AP_fbcm_index) / len(AP_fbcm_index))

    def parse_sample(self, RSSISamples) -> SimpleLocation:
        """evaluate
        this methode goes trough a sample and compute it's distance
         :param RSSISamples : an RSSISample containing data taken from one of the ap used to calibrate the model
         :return: The evaluated distance
        """
        # list of distances with each access points
        distances = []

        # run through the AP list
        for j in range(0, len(self.APs)):
            temp_dist = []

            # run through the list of RSSI values
            for i in range(0, len(RSSISamples)):

                # search for RSSI value that correspond to the AP
                if RSSISamples[i].mac_address == self.APs[j].mac_address:
                    # estimate the distance using Friis index
                    dist = FBCM.estimate_distance(RSSISamples[i].avg_rssi, self.fbcm_index[j],
                                                  self.APs[j])

                    # append to the list of distances
                    temp_dist.append(dist)
                    break

            # if list not empty, add the mean value of the list
            if len(temp_dist) != 0:
                distances.append(sum(temp_dist) / len(temp_dist))
            else:
                # otherwise return -1 for error
                distances.append(-1)

        # extracts locations of APs
        locations_list = [access_point.location for access_point in self.APs]

        # search for the location of the sample giving AP location and estimated distances with them
        pos = self.beta_multilateration(distances, locations_list)
        return pos

    def compute_FBCM_index(self, distance: float, rssi: RSSISample, ap: AccessPoint) -> float:
        """Function compute_FBCM_index computes a FBCM index based on the distance (between transmitter and receiver)
        and the AP parameters. We consider the mobile device's antenna gain is 2.1 dBi.
        :param ap: Acess point
        :param distance: the distance between AP and device
        :param rssi: the RSSI values associated to the AP for current calibration point. Use their average value.
        :return: one value for the FBCM index
        """

        # Add a check to avoid negative or zero arguments for the logarithm
        if distance <= 0:
            print("Error: distance <= 0. Value rounded to 0.0001")
            distance = 0.0001

        GAIN = 2.1
        GTX = ap.antenna_dbi
        wavelength = 299792458 / ap.output_frequency_hz
        PR = rssi.avg_rssi
        PT = ap.output_power_dbm
        # Calculating the numerator of the formula
        index = PT - PR + GAIN + GTX + 20 * log10(wavelength / 4 * pi)
        index = index / (10 * log(distance))
        return index

    @staticmethod
    def estimate_distance(rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
        """
        Function estimate_distance estimates the distance between an access point and a test point based on
        the test point rssi sample.
        :param rssi: average RSSI value for test point
        :param fbcm_index: index to use
        :return: the distance (meters)
        """

        GAIN = 2.1
        GT = ap.antenna_dbi
        PR = rssi_avg
        PT = ap.output_power_dbm
        l = 299792458 / ap.output_frequency_hz

        estimated_distance = pow(10, (PT - PR + GT + GAIN + 20 * log10(l / (4 * pi))) / (10 * fbcm_index))
        return estimated_distance

    @staticmethod
    def beta_multilateration(distances: list[float], ap_locations: list[SimpleLocation]) -> SimpleLocation:
        """
        Perform multilateration to compute the location based on distances and access point locations.
        :param distances: List of distances between the sample and each access point
        :param ap_locations: List of access point locations
        :return: Computed location as a SimpleLocation object
        """

        def objective_function(location: np.ndarray) -> np.ndarray:
            """
            Objective function for the optimization process.
            Calculates the differences between estimated distances and actual distances.
            :param location: Input location to evaluate as an np.ndarray
            :return: Differences between estimated distances and actual distances as an np.ndarray
            """
            location_obj = SimpleLocation(location[0].real, location[1].real, location[2].real)
            return np.array([
                SimpleLocation.evaluateDistance(location_obj, loc) - dist
                for dist, loc in zip(distances, ap_locations)
            ])

        initial_guess = SimpleLocation(0, 0, 0)  # Starting point for optimization

        # Optimize the objective function using least squares (Levenberg-Marquardt algorithm)
        result = least_squares(objective_function, [initial_guess.x, initial_guess.y, initial_guess.z], xtol=1e-15,
                               ftol=1e-15, max_nfev=1000)

        # Extract the optimized location
        optimized_location = result.x

        return SimpleLocation(*optimized_location)

    @staticmethod
    def multilateration(distances: list[float], ap_locations: list[SimpleLocation], invp: int = 2) -> SimpleLocation:
        """_multilateration
        this methode return a location that is not that far from each
            distances : list of distances between the sample and each access point
            ap_locations : list of locations of each access point
        """
        # get the maximum distance of each AP in order to draw the rectangle of possibilities
        maxd = max(distances) + 1

        # compute the min, max edges on each coordinates.
        minx = int(min([loc.x for loc in ap_locations]) - maxd)
        miny = int(min([loc.y for loc in ap_locations]) - maxd)
        minz = int(min([loc.z for loc in ap_locations]) - maxd)

        maxx = int(max([loc.x for loc in ap_locations]) + maxd)
        maxy = int(max([loc.y for loc in ap_locations]) + maxd)
        maxz = int(max([loc.z for loc in ap_locations]) + maxd)

        # get the precision
        precision = 1 / invp

        # number of APs
        N = len(distances)
        # set initial minium distance (big one)
        minDist = 10000000000000000
        # set initial min location
        minPos = SimpleLocation(0, 0, 0)

        # run through x, y, z range in order to evaluate the best location
        for xint in range(minx * invp, maxx * invp):
            x = xint * precision
            for yint in range(miny * invp, maxy * invp):
                y = yint * precision
                for zint in range(minz * invp, maxz * invp):
                    z = zint * precision

                    # location to evaluate
                    p = SimpleLocation(x, y, z)
                    sum = 0
                    for i in range(0, N):
                        # sum up the distances of the location with each range of each AP given the estimated distance
                        # -1 mean that the distance failled be computed
                        if distances[i] != -1:
                            sum += abs(SimpleLocation.evaluateDistance(p, ap_locations[i]) - distances[i])

                    # store the position if the sum is the lowest
                    if sum < minDist:
                        minDist = sum
                        minPos = p
        return minPos
