from numpy import ComplexWarning

from TD_package.FingerprintDatabase import FingerprintDatabase
from TD_package.AccessPoint import AccessPoint
from TD_package.SimpleLocation import SimpleLocation
from TD_package.FBCM import FBCM

# Variable and data initialisation
AP = [AccessPoint("00:13:ce:95:e1:6f", SimpleLocation(4.93, 25.81, 3.55)),
      AccessPoint("00:13:ce:95:de:7e", SimpleLocation(4.83, 10.88, 3.78)),
      AccessPoint("00:13:ce:97:78:79", SimpleLocation(20.05, 28.31, 3.74)),
      AccessPoint("00:13:ce:8f:77:43", SimpleLocation(4.13, 7.085, 0.80))
    #,AccessPoint("00:13:ce:8f:78:d9", SimpleLocation(5.74, 30.35, 2.04))
      ]

# Calibration data used in TD1
db_calibration = FingerprintDatabase()
db_calibration.read_csv('data.csv')
db_calibration.compute_avg_all()
db_calibration.to_csv_bis('output.csv')

# Test data
db_test = FingerprintDatabase()
db_test.read_csv('test_data.csv')
db_test.compute_avg_all()

fbcm_handler = FBCM(AP, db_calibration.db)

# Evaluating the test data using the FBCM model
sum = 0
N = 0
for finger in db_test.db:

    RSSI = finger.samples
    print('Real location : \t' + str(finger.position))

    # Compute the distance
    pos_est = fbcm_handler.parse_sample(RSSI)
    print('Estimated location : \t' + str(pos_est))

    # compute distance between real location and the estimated one
    dist = SimpleLocation.evaluateDistance(pos_est, finger.position)
    print('Error distance : \t' + str(dist))

    N += 1
    sum += dist
    # print()

print("Average : " + str(sum / N))
