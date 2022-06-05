import machine, time
from machine import Pin

__version__ = '0.2.0'
__author__ = 'Roberto Sánchez'
__license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"

class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.

    The timeouts received listening to echo pin are converted to OSError('Out of range')

    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin. 
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()
 
        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        mm = pulse_time * 100 // 582
        return mm

    def vitesse(self,waitfor = 30000):
        """
        Get the speed in m/s
        """
        vitesse = None
        
        
        pulse1_time = -1
        pulse2_time = -1
        delta_time = 100000
        while pulse1_time<0 or pulse2_time<0 or abs(delta_time)>300 :
#            print('---------------------------------------------------------')
            t1_1 = time.ticks_us()
            pulse1_time = self._send_pulse_and_wait()
            t1_2 = time.ticks_us()
#            print('temps de la premiere mesure', t1_2-t1_1)
            time.sleep_us(waitfor)
            t2_1 = time.ticks_us()
            pulse2_time = self._send_pulse_and_wait()
            t2_2 = time.ticks_us()
#            print('temps de la deuxieme mesure', t2_2-t2_1)
            delta_time = pulse2_time - pulse1_time
            

        
        mean_pulse = (pulse2_time + pulse1_time)/2
        vitesse = delta_time * 343.20 / (waitfor+mean_pulse) 
        distance = pulse1_time * 100 // 582
#        print('pulse1_time = ',pulse1_time)
#        print('pulse2_time = ',pulse2_time)
#        print('mean_pulse = ',mean_pulse)
#        print('delta_time = ',delta_time)
#        print('vitesse = ',vitesse)
#        print('distance = ',distance)
        return  distance, time.ticks_us(), vitesse

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms

