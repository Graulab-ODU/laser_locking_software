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
    def set_wavelength(self, setpoint_, Kp=626, Ki=613.6363, Kd=0, time_running=0, interval_delay=0.2, max_voltage=130, min_voltage=30, max_voltage_change=5):
        
        #because of how decreasing voltage increases the wavelength, Kp and Ki must be negative
        Kp = min(Kp, Kp*-1)
        Ki = min(Ki, Ki*-1)
        
        pid = PID(Kp, Ki, Kd, setpoint=setpoint_)
        change = 0

        
        previous_wavelength = self.get_wavelength()
        
        for i in range(9000):    

            st=time.time()

            #protects the program from crashing if the laser enters multi-mode/connection time outs
            try:
                wavelength = self.get_wavelength()
            except:
                wavelength = previous_wavelength
            if (type(wavelength) != float):
                wavelength = previous_wavelength

            #adds deadzone to the wavelength value
            wavelength = float(int(wavelength*100000))/100000

            #Runs the PID
            change = pid(wavelength)   

            #makes sure the change in voltage is not beyond the given max change
            change = self._interval_clamp(change, max_voltage_change*-1, max_voltage_change)


            #calculates what the new voltage offset will be and keeps it in a specific interval
            new_voltage = self._interval_clamp(self.get_voltage_offset()+(change), min_voltage, max_voltage)

            #alters the voltage according to the change from the pid
            self.set_voltage_offset(new_voltage)

            #updates previous_wavelength
            if (type(wavelength) == float):
                previous_wavelength = wavelength
            
            #ensure the program pauses is equal to the given interval_delay or how long the program takes to run
            et = time.time()
            time.sleep((interval_delay-(et-st)) if (interval_delay-(et-st)) > 0 else 0)





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