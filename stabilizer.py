from moglabs_fzw import Wavemeter
from DLC_Pro_Controller import Laser

class Stabalizer:
    
    _wavemeter = None
    _wavemeter_address = None
    _laser_network = None
    _DLC_Pro = None

    def __init__(self, wavemeter_address, network_address, laser_controller):
        self._wavemeter_address = wavemeter_address
        
        #sets up connecting to the wavemeter
        self._wavemeter = Wavemeter(wavemeter_address)

        # sets up connection to the DLC_Pro_Controller
        self._DLC_Pro = Laser(network_address, laser_controller)
        
        
