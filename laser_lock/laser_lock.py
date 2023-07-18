from moglabs_fzw import Wavemeter
from DLC_Pro_Controller import Laser
from simple_pid import PID

class Laser_lock:
    #possible DLC controllers: Barium, Photoionization, Lutetium_848nm_1244nm, Lutetium_646nm

    # laser wavelength in nm        493          650                646                     646                     848
    _wavemeter_port_reference=[['Barium', 1], ['Barium', 2], ['Lutetium_646nm', 2], ['Lutetium_646nm', 1], ['Lutetium_848nm_1244nm', 2]]# ports 6, 7, 8 are not set up as of yet
    _wavemeter_channel = 1

    _wavemeter = None
    _wavemeter_address = None
    _laser = None

    def __init__(self, wavemeter_address, network_address, laser_controller, laser_number):
        self._wavemeter_address = wavemeter_address
        
        #sets up connecting to the wavemeter
        self._wavemeter = Wavemeter(wavemeter_address)

        # sets up connection to the DLC_Pro_Controller and laser
        self._laser = Laser(network_address, laser_controller, laser_number)

        #finds the proper wavemeter port
        for i in range(len(self._wavemeter_port_reference)):
            if (self._wavemeter_port_reference[i] == [laser_controller, laser_number]):
                self.wavemeter_channel = i + 1
                return
        raise Exception("Laser not connected to the Wavemeter")
    
    # will lock the lasers to a certain wavelength
    def set_wavelength(self, setpoint_, Kp=0.5, Ki=0.05, Kd=0):
        pass
        '''Untested, do not run'''
        
        pid = PID(Kp, Ki, Kd, setpoint=setpoint_)

        change = 0
        while True:    #find a proper way to run and end the loop
            
            change = pid(self.get_wavelength() + change)

            #maybe enter a time sleep function






    # gets laser wavelength
    def get_wavelength(self, channel=1):
        return self._wavemeter[channel]
    
    # gets the laser voltage offset
    def get_voltage_offset(self):
        return self._laser.get_voltage_offset()
    
    #sets the laser votage offset
    def set_voltage_offset(self, offset):
        self._laser.set_voltage_offset(offset)

    #returns wavemeter port
    def get_wavemeter_port(self):
        return self._wavemeter_channel