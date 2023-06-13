from .FingerprintSample import FingerprintSample
from .SimpleLocation import SimpleLocation


class Fingerprint(FingerprintSample):
    def __init__(self, position: SimpleLocation) -> None:
        self.position = position
        super().__init__([])
