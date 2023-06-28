from moglabs_fzw import Wavemeter
from DLC_Pro_Controller import Laser

class Laser_locking:
    
    _wavemeter = None
    _wavemeter_address = None
    _laser = None

    def __init__(self, wavemeter_address, network_address, laser_controller, laser_number):
        self._wavemeter_address = wavemeter_address
        
        #sets up connecting to the wavemeter
        self._wavemeter = Wavemeter(wavemeter_address)

        # sets up connection to the DLC_Pro_Controller and laser
        self._laser = Laser(network_address, laser_controller, laser_number)
        
    
    # will lock the lasers to a certain wavelength
    def set_wavelength(self, setpoint):
        pass






    # gets laser wavelength
    def get_wavelength(self, channel=1):
        return self._wavemeter[channel]
    
    # gets the laser voltage offset
    def get_voltage_offset(self):
        return self._laser.get_voltage_offset()
    
    #sets the laser votage offset
    def set_voltage_offset(self, offset):
        self._laser.set_voltage_offset(offset)