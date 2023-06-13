from .SimpleLocation import SimpleLocation


class AccessPoint:
    def __init__(self, mac: str, loc: SimpleLocation) -> None:
        self.mac_address = mac
        self.location = loc
        self.output_power_dbm = 20.0
        self.antenna_dbi = 5.0
        self.output_frequency_hz = 2417000000.0
