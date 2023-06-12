from cmath import log
from scipy.optimize import least_squares
import numpy as np
from TD_package.RSSISample import RSSISample
from TD_package.AccessPoint import AccessPoint
from TD1.TD_package.SimpleLocation import SimpleLocation

import math import pi


class FBCM:

    def __init__(self, AP_list, calibration_data)-> None:
        self.AP = AP_list

   def __init__(self, AP_list, fingerprint_list) -> None:
        """Constructor
            AP_list : list of AP present
            fingerprint_list : list of fingerprint to calibrate
        Construct the object, and calibrate the model for the given dataset and access points
        the list of fingerprint is used only for calibration and is dump after
        """
        # list of Access points
        self._AP_list = AP_list

        # list of fingerprint (used only for calibration)
        self._fbcm_index = []

        # run through the Access point list
        for AP_n in self._AP_list:

            # temporary list of indexes
            AP_fbcm_index = []

            # run through the fingerprint list
            for fingerprint_n in fingerprint_list:

                # evaluate the real distance between the fingerprint and the AP
                distance = evaluateDistance(fingerprint_n.location, AP_n.location)

                # run through the RSSI Sample list
                for rssiSample in fingerprint_n._RSSISample_list:
                    
                    #look for RSSI Samples that concern the AP (corresponding mac address)
                    if rssiSample.mac_address == AP_n.mac_address:
                        # compute index with this sample and knowing the distance. 
                        # I firstly tried to filter long distances when rssi is hign
                        if rssiSample.get_average_rssi() > -80:
                            AP_POS_fbcm_index = _compute_FBCM_index(distance, rssiSample, AP_n)
                            break

                # adding index to the list
                # I choose to filter indexes between 3 and 3.5
                if AP_POS_fbcm_index > 2 and AP_POS_fbcm_index < 3.5:
                    AP_fbcm_index.append(AP_POS_fbcm_index)
            
            # averaging indexes
            self._fbcm_index.append(sum(AP_fbcm_index)/len(AP_fbcm_index))     
        
    
    def compute_FBCM_index(distance: float, rssi: RSSISample, ap: AccessPoint) -> float:
        """Function compute_FBCM_index computes a FBCM index based on the distance (between transmitter and receiver)
        and the AP parameters. We consider the mobile device's antenna gain is 2.1 dBi.
        :param distance: the distance between AP and device
        :param rssi_values: the RSSI values associated to the AP for current calibration point. Use their average value.
        :return: one value for the FBCM index
        """
        GAIN = 2.1
        GTX = ap.antenna_dbi
        wavelength = 299792458 / ap.output_frequency_hz
        PR = rssi.avg_rssi
        PT = ap.output_power_dbm
        #Calculating the numerator of the formula
        index = PT - PR + GAIN + GTX + 20*log(wavelength/4* pi)
        index = index / 10 * log (distance)
        return index
    
    def estimate_distance(rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
        """
        Function estimate_distance estimates the distance between an access point and a test point based on
        the test point rssi sample.
        :param rssi: average RSSI value for test point
        :param fbcm_index: index to use
        :param ap: access points parameters used in FBCM
        :return: the distance (meters)
        """

        GAIN = 2.1
        GT = ap.antenna_dbi
        PR = rssi_avg
        PT = ap.output_power_dbm
        l = 299792458 / ap.output_frequency_hz
    
        estimated_distance = pow(10, (PT - PR + GT + GAIN +20*log( l/(4*pi) )) / (10 * fbcm_index))
        return estimated_distance
    
    def multilateration(distances: list[float], ap_locations: list[SimpleLocation]) -> SimpleLocation:
        """
        Perform multilateration to compute the location based on distances and access point locations.
        :param distances: List of distances between the sample and each access point
        :param ap_locations: List of access point locations
        :return: Computed location as a SimpleLocation object
        """
        def objective_function(location: SimpleLocation) -> np.ndarray:
            """
            Objective function for the optimization process.
            Calculates the differences between estimated distances and actual distances.
            :param location: Input location to evaluate
            :return: Differences between estimated distances and actual distances as an np.ndarray
            """
            return np.array([
                SimpleLocation.evaluateDistance(location, loc) - dist
                for dist, loc in zip(distances, ap_locations)
            ])

        initial_guess = SimpleLocation(0, 0, 0)  # Starting point for optimization

        # Optimize the objective function using least squares
        result = least_squares(objective_function, [initial_guess.x, initial_guess.y, initial_guess.z])

        # Extract the optimized location
        optimized_location = result.x

        return SimpleLocation(*optimized_location)