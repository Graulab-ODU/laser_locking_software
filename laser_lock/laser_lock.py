from moglabs_fzw import Wavemeter
from DLC_Pro_Controller import Laser
from simple_pid import PID

import time

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
                self._wavemeter_channel = i + 1
                return
        raise Exception("Laser not connected to the Wavemeter")
    
    # will lock the lasers to a certain wavelength
    def set_wavelength(self, setpoint_, Kp=1, Ki=0.05, Kd=0, max_voltage=100, min_voltage=0, max_voltage_change=1):
        
        #because of how decreasing voltage increases the wavelength, Kp and Ki must be negative
        Kp = min(Kp, Kp*-1)
        Ki = min(Ki, Ki*-1)
        
        pid = PID(Kp, Ki, Kd, setpoint=setpoint_)
        change = 0

        x='4'
        previous_wavelength = self.get_wavelength(self._wavemeter_channel)
        
        while (x != 'end'):    #find a proper way to run and end the loop

            #protects the program from crashing if the laser enters multi-mode
            wavelength = self.get_wavelength(self._wavemeter_channel)
            if (type(wavelength) != float):
                wavelength = previous_wavelength

            #Runs the PID
            change = pid(wavelength)   

            #makes sure the change in voltage is not beyond the given max change
            change = self._interval_clamp(change, max_voltage_change*-1, max_voltage_change)


            #calculates what the new voltage offset will be and keeps it in a specific interval
            new_voltage = self._interval_clamp(self.get_voltage_offset()+(change), min_voltage, max_voltage)

            #alters the voltage according to the change from the pid
            #self.set_voltage_offset(change)  #perhaps I should alter the change such as devide it in half?
            print('recommended voltage: ', new_voltage)
            x=input()

            #updates previous_wavelength
            previous_wavelength = wavelength
            
        





    # returns laser's wavelength in nm(vac)
    def get_wavelength(self):
        return self._wavemeter[self._wavemeter_channel].wavelength
    
    # gets the laser voltage offset
    def get_voltage_offset(self):
        return self._laser.get_voltage_offset()
    
    #sets the laser votage offset
    def set_voltage_offset(self, offset):
        self._laser.set_voltage_offset(offset)

    #returns wavemeter port
    def get_wavemeter_port(self):
        return self._wavemeter_channel
    
    #will return the value if it is in the given interval, or the value closest to it in the interval
    def _interval_clamp(self, x, minval, maxval):
        return min(max(x, minval), maxval)