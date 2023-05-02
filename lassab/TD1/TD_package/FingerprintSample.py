from TD_package.RSSISample import RSSISample
import string

class FingerprintSample:
    def __init__(self, samples: list[RSSISample]) -> None:
        self.samples = samples
    
    def add(self, rssi_value : float, mac_address : string ):
        """
		add a new RSSI sample to the list
        if an RSSI sample with the same mac address already exist, add it the RSSI value
		"""
        # Check if we found a sample with the same mac address
        for RSSISample_parser in self.samples:
            if RSSISample_parser.mac_address == mac_address:
    			# Associate this RSSI with the mac address we found
                RSSISample_parser.add(rssi_value)
                #Since there can only be one match, we stop the parsing
                return
        
    	# No match found, create a new sample 
        new_sample = RSSISample(mac_address)
        new_sample.add(rssi_value)
        self.samples.append(new_sample)
