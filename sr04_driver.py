# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

from machine import Pin, time_pulse_us
from time import sleep_us, sleep_ms

class SR04:
    """
    The SR04 Ultrasonic Distance Sensor Driver
    """

    class SR04_MEASURE_TIMEOUT(Exception): pass

    _echo_pin:Pin = None
    _trig_pin:Pin = None
    _speed_of_sound_fixed:float = None

    def __init__(self, pin_echo:Pin, pin_trig:Pin, speed_of_sound:int=340) -> None:
        """
        **Constructor of Driver**
        :param pin_echo: SR04's echo pin.
        :param pin_trig: SR04's trig pin.
        :param speed_of_sound: speed of soun in m/s. Default is 340m/s.
        """
        self._echo_pin = pin_echo
        self._trig_pin = pin_trig

        self._echo_pin.init(mode=Pin.IN)
        self._trig_pin.init(mode=Pin.OUT, value=0)

        self._speed_of_sound_fixed = speed_of_sound / 20000   # from m/s to cm/μs and divided 2, see
                                                              # measure_centimeter() func.

        sleep_ms(1000)

    def measure_centimeter(self) -> float:
        """
        Measure distance in centimeter.
        :return: distance in centimeter, with 1 decimal place. SR04's accuracy is 3mm.
        """
        # send 10μs pulse to measure
        self._trig_pin.on()
        sleep_us(10)
        self._trig_pin.off()

        echo_time = time_pulse_us(self._echo_pin,
                                  1,
                                  17650)    # max measuring distance is 4 meter. Here is 1.5 times the return
                                                      # time at the maximum distance.

        if echo_time < 0 : raise self.SR04_MEASURE_TIMEOUT

        return round(echo_time * self._speed_of_sound_fixed, # distance = echo_time / 2 * <speed_of_sound>
                     1)  # The accuracy is 3mm, with 1 decimal place.


