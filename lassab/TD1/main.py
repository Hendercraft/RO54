from TD_package.FingerprintDatabase import FingerprintDatabase
from TD_package.AccessPoint import AccessPoint
from TD_package.SimpleLocation import SimpleLocation



AP = {"00:13:ce:95:e1:6f": AccessPoint("00:13:ce:95:e1:6f", SimpleLocation(4.93, 25.81, 3.55)), \
      "00:13:ce:95:de:7e": AccessPoint("00:13:ce:95:de:7e", SimpleLocation(4.83, 10.88, 3.78)), \
      "00:13:ce:97:78:79": AccessPoint("00:13:ce:97:78:79", SimpleLocation(20.05, 28.31, 3.74)), \
      "00:13:ce:8f:77:43": AccessPoint("00:13:ce:8f:77:43", SimpleLocation(4.13, 7.085, 0.80)), \
      "00:13:ce:8f:78:d9": AccessPoint("00:13:ce:8f:78:d9", SimpleLocation(5.74, 30.35, 2.04))}

db = FingerprintDatabase()
db.read_csv('data.csv')
db.compute_avg_all()
db.to_csv_bis('output.csv')