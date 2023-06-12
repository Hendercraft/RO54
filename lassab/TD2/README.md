# TD2: GNSS-like systems

This TD uses the data structures from TD1.

## Access Points data

You will add an AccessPoint class with the desired members to build and access AP data. Your class is based on the following fields:

```python
class AccessPoint:
	def __init__(self, mac: str, loc=Location(): Location, p=20.0: float, a=5.0: float, f=2417000000: float):
		self.mac_address = mac
		self.location = loc
		self.output_power_dbm = p
		self.antenna_dbi = a
		self.output_frequency_hz = f
```

AP data will be static, such like this:

```python
AP = {"00:13:ce:95:e1:6f": AccessPoint("00:13:ce:95:e1:6f", 4.93, 25.81, 3.55, 2417000000, 5.0, 20.0), \
      "00:13:ce:95:de:7e": AccessPoint("00:13:ce:95:de:7e", 4.83, 10.88, 3.78, 2417000000, 5.0, 20.0), \
      "00:13:ce:97:78:79": AccessPoint("00:13:ce:97:78:79", 20.05, 28.31, 3.74, 2417000000, 5.0, 20.0), \
      "00:13:ce:8f:77:43": AccessPoint("00:13:ce:8f:77:43", 4.13, 7.085, 0.80, 2417000000, 5.0, 20.0), \
      "00:13:ce:8f:78:d9": AccessPoint("00:13:ce:8f:78:d9", 5.74, 30.35, 2.04, 2417000000, 5.0, 20.0)}
```

## Computing FBCM index

In this part, you have to compute the FBCM index given a distance between a transmitter and a receiver, and its RSSISample.

```python
def compute_FBCM_index(distance: float, rssi_values: RSSISample, ap: AccessPoint) -> float:
	"""
    Function compute_FBCM_index computes a FBCM index based on the distance (between transmitter and receiver)
    and the AP parameters. We consider the mobile device's antenna gain is 2.1 dBi.
    :param distance: the distance between AP and device
    :param rssi_values: the RSSI values associated to the AP for current calibration point. Use their average value.
    :return: one value for the FBCM index
    """
	pass
```

## Computing a distance based on a RSSISample

Here, you have to implement the following function, which takes an average RSSI value for a transmitter and a receiver, a FBCM index matching the sample and the corresponding AP data. Consider a 2.1 dBi gain for the device.
```python
def estimate_distance(rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
    """
    Function estimate_distance estimates the distance between an access point and a test point based on
    the test point rssi sample.
    :param rssi: average RSSI value for test point
    :param fbcm_index: index to use
    :param ap: access points parameters used in FBCM
    :return: the distance (meters)
    """
	pass
```

## Getting a location

With distances between a device and at least 3 references, compute device's location. You may use grid search, or python solver (least squares, etc.)

```python
def multilateration(distances: dict[str, float], ap_locations: dict[str, Location]) -> Location:
    """
    Function multilateration computes a location based on its distances towards at least 3 access points
    :param distances: the distances associated to the related AP MAC addresses as a string
    :param ap_locations: the access points locations, indexed by AP MAC address as strings
    :return: a location
    """
	pass
```

## Main

Use all functions to provide compute locations for the test data set provided with these instructions (calibration data will be TD1 data).
