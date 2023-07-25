from moglabs_fzw import Wavemeter
from DLC_Pro_Controller import Laser
from simple_pid import PID

import time
import matplotlib.pyplot as plt

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
        
        '''Untested, do not run'''
        
        pid = PID(Kp, Ki, Kd, setpoint=setpoint_)
        change = 0

        x='4'
        st = time.time()

        t_time=[]
        wavelength=[]
        
        while (x != 'end'):    #find a proper way to run and end the loop
            t_time.append(st-time.time())


            #finds the change from the PID
            change = pid(self.get_wavelength(self._wavemeter_channel))

            #makes sure the change in voltage is not beyond the given interval
            if (max_voltage_change > (change/2) > 0):
                change = 1 #20/2 = 10


            #calculates what the new voltage offset will be
            change = self.get_voltage_offset()+(change/2)

            #sets up limitations for the PID to make sure it doesnt go beyond or break certain things
            if (max_voltage > (change/2) > min_voltage):
                change = 70


            #alters the voltage according to the change from the pid
            #self.set_voltage_offset(change)  #perhaps I should alter the change such as devide it in half?
            print('recommended voltage: ', change/2)
            x=input()
        plt.plot(t_time, wavelength)
        plt.xlabel('time (s)')
        plt.ylabel('wavelength')
        plt.title('PID indirectly influencing wavelength with excess noise')
        plt.show()





    # gets laser wavelength
    def get_wavelength(self, channel):
        return self._wavemeter[channel].wavelength
    
    # gets the laser voltage offset
    def get_voltage_offset(self):
        return self._laser.get_voltage_offset()
    
    #sets the laser votage offset
    def set_voltage_offset(self, offset):
        self._laser.set_voltage_offset(offset)

    #returns wavemeter port
    def get_wavemeter_port(self):
        return self._wavemeter_channel