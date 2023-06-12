from TD_package.RSSISample import RSSISample
import string


class FingerprintSample:
    def __init__(self, samples: list[RSSISample]) -> None:
        self.samples = samples

    def add(self, rssi_value: float, mac_address: string):
        """
        add a new RSSI sample to the list
        if an RSSI sample with the same mac address already exist, add it the RSSI value
        """
        sample = self.get_RSSIsample(mac_address)
        if sample is not None:
            sample.add(rssi_value)
            return
        else:
            # No match found, create a new sample 
            new_sample = RSSISample(mac_address)
            new_sample.add(rssi_value)
            self.samples.append(new_sample)

    def get_RSSIsample(self, mac_address: string) -> RSSISample or None:
        for RSSISample_parser in self.samples:
            if RSSISample_parser.mac_address == mac_address:
                return RSSISample_parser
        return None
