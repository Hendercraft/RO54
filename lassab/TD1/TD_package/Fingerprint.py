from TD_package.FingerprintSample import FingerprintSample
from TD_package.SimpleLocation import SimpleLocation

class Fingerprint(FingerprintSample):
    def __init__(self, position: SimpleLocation) -> None:
        self.position = position
        super().__init__([])