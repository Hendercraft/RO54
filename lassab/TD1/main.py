from TD_package.FingerprintDatabase import FingerprintDatabase

db = FingerprintDatabase()
db.read_csv('data.csv')
db.compute_avg_all()
db.to_csv_bis('output.csv')