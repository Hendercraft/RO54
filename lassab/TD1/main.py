from TD_package.FingerprintDatabase import FingerprintDatabase
from TD_package.AccessPoint import AccessPoint
from TD_package.SimpleLocation import SimpleLocation
from TD_package.FBCM import FBCM
AP = [AccessPoint("00:13:ce:95:e1:6f", SimpleLocation(4.93, 25.81, 3.55)),
      AccessPoint("00:13:ce:95:de:7e", SimpleLocation(4.83, 10.88, 3.78)),
      AccessPoint("00:13:ce:97:78:79", SimpleLocation(20.05, 28.31, 3.74)),
      AccessPoint("00:13:ce:8f:77:43", SimpleLocation(4.13, 7.085, 0.80)),
      AccessPoint("00:13:ce:8f:78:d9", SimpleLocation(5.74, 30.35, 2.04))]

#Calibration data used in TD1
db_calibration = FingerprintDatabase()
db_calibration.read_csv('data.csv')
db_calibration.compute_avg_all()
db_calibration.to_csv_bis('output.csv')

fbcm_handler = FBCM(AP,db_calibration.db)