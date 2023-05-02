from TD_package.FingerprintDatabase import FingerprintDatabase
from TD_package.AccessPoint import AccessPoint



AP = {"00:13:ce:95:e1:6f": AccessPoint("00:13:ce:95:e1:6f", 4.93, 25.81, 3.55, 2417000000, 5.0, 20.0), \
      "00:13:ce:95:de:7e": AccessPoint("00:13:ce:95:de:7e", 4.83, 10.88, 3.78, 2417000000, 5.0, 20.0), \
      "00:13:ce:97:78:79": AccessPoint("00:13:ce:97:78:79", 20.05, 28.31, 3.74, 2417000000, 5.0, 20.0), \
      "00:13:ce:8f:77:43": AccessPoint("00:13:ce:8f:77:43", 4.13, 7.085, 0.80, 2417000000, 5.0, 20.0), \
      "00:13:ce:8f:78:d9": AccessPoint("00:13:ce:8f:78:d9", 5.74, 30.35, 2.04, 2417000000, 5.0, 20.0)}

db = FingerprintDatabase()
db.read_csv('data.csv')
db.compute_avg_all()
db.to_csv_bis('output.csv')