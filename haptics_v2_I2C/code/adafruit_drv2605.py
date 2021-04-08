# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_drv2605`
====================================================

CircuitPython module for the DRV2605 haptic feedback motor driver.  See
examples/simpletest.py for a demo of the usage.

* Author(s): Tony DiCola
"""
from micropython import const

from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_DRV2605.git"


##
# EDITED BY github: @MISSCRISPENCAKES
# FOR LRA CLOSED-LOOP DEFAULT 
# AUTO-CALIB SETUP
##

import coloredlogs, logging

# Creating logger
mylogs = logging.getLogger(__name__)
mylogs.setLevel(logging.DEBUG)

fieldstyle = {'asctime': {'color': 'green'},
              'levelname': {'bold': True, 'color': 'black'},
              'filename':{'color':'cyan'},
              'funcName':{'color':'blue'}}
                                   
levelstyles = {'critical': {'bold': True, 'color': 'red'},
               'debug': {'color': 'green'}, 
               'error': {'color': 'red'}, 
               'info': {'color':'magenta'},
               'warning': {'color': 'yellow'}}

# Handler - 1
file = logging.FileHandler("Sample.log")
fileformat = logging.Formatter("%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s")#%(asctime)s:%(levelname)s:%(message)s")
file.setLevel(logging.WARNING)
file.setFormatter(fileformat)

# Handler - 2
cric_file = logging.FileHandler("Critical.log")
cric_file.setLevel(logging.CRITICAL)
cric_file.setFormatter(fileformat)

# Handler - 3
coloredlogs.install(level=logging.DEBUG,
                    logger=mylogs,
                    fmt='%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s',
                    datefmt='%H:%M:%S',
                    field_styles=fieldstyle,
                    level_styles=levelstyles)

# Adding all handlers to the logs
mylogs.addHandler(file)
mylogs.addHandler(cric_file)

# Some demo codes
mylogs.debug("debug")
mylogs.info("info")
mylogs.warning("warn")
mylogs.critical("critical")
mylogs.error("error")


# Internal constants:
_DRV2605_ADDR = const(0x5A)
_DRV2605_REG_STATUS = const(0x00)
_DRV2605_REG_MODE = const(0x01)

_DRV2605_REG_RTPIN = const(0x02)

_DRV2605_REG_LIBRARY = const(0x03)
_DRV2605_REG_WAVESEQ1 = const(0x04)
_DRV2605_REG_WAVESEQ2 = const(0x05)
_DRV2605_REG_WAVESEQ3 = const(0x06)
_DRV2605_REG_WAVESEQ4 = const(0x07)
_DRV2605_REG_WAVESEQ5 = const(0x08)
_DRV2605_REG_WAVESEQ6 = const(0x09)
_DRV2605_REG_WAVESEQ7 = const(0x0A)
_DRV2605_REG_WAVESEQ8 = const(0x0B)

_DRV2605_REG_GO = const(0x0C)

_DRV2605_REG_OVERDRIVE = const(0x0D)
_DRV2605_REG_SUSTAINPOS = const(0x0E)
_DRV2605_REG_SUSTAINNEG = const(0x0F)
_DRV2605_REG_BREAK = const(0x10)

_DRV2605_REG_AUDIOCTRL = const(0x11)
_DRV2605_REG_AUDIOMINLV = const(0x12)
_DRV2605_REG_AUDIOMAXLV = const(0x13)
_DRV2605_REG_AUDIOMINDR = const(0x14)
_DRV2605_REG_AUDIOMAXDR = const(0x15)

_DRV2605_REG_RATEDV = const(0x16)
_DRV2605_REG_CLAMPV = const(0x17)
_DRV2605_REG_AUTOCALCOMP = const(0x18)
_DRV2605_REG_AUTOCALEMP = const(0x19)

_DRV2605_REG_FEEDBACK = const(0x1A)
_DRV2605_REG_CONTROL1 = const(0x1B)
_DRV2605_REG_CONTROL2 = const(0x1C)
_DRV2605_REG_CONTROL3 = const(0x1D)
_DRV2605_REG_CONTROL4 = const(0x1E)
_DRV2605_REG_CONTROL5 = const(0x1F)

_DRV2605_REG_LRAOPEN = const(0x20)
_DRV2605_REG_VBAT = const(0x21)
_DRV2605_REG_LRARESON = const(0x22)

# User-facing mode value constants:
MODE_INTTRIG = 0x00
MODE_EXTTRIGEDGE = 0x01
MODE_EXTTRIGLVL = 0x02
MODE_PWMANALOG = 0x03
MODE_AUDIOVIBE = 0x04
MODE_REALTIME = 0x05
MODE_DIAGNOS = 0x06
MODE_AUTOCAL = 0x07

MODE_STANDBY = 0x40

LIBRARY_EMPTY = 0x00
LIBRARY_TS2200A = 0x01
LIBRARY_TS2200B = 0x02
LIBRARY_TS2200C = 0x03
LIBRARY_TS2200D = 0x04
LIBRARY_TS2200E = 0x05
LIBRARY_LRA = 0x06


class DRV2605:
    """TI DRV2605 haptic feedback motor driver module."""

    # Class-level buffer for reading and writing data with the sensor.
    # This reduces memory allocations but means the code is not re-entrant or
    # thread safe!
    _BUFFER = bytearray(2)

    def __init__(self, i2c, address=_DRV2605_ADDR):
        self._device = I2CDevice(i2c, address)
        # Check chip ID is 3 or 7 (DRV2605 or DRV2605L).
        status = self._read_u8(_DRV2605_REG_STATUS)
        device_id = (status >> 5) & 0x07
        mylogs.info("2605 (3) or 2605L (7): {}".format(device_id))
        if device_id not in (3, 7):
            mylogs.critical("Failed to find DRV2605, check wiring!")
            raise RuntimeError("Failed to find DRV2605, check wiring!")
          
        # Configure registers to initialize chip.
        self._write_u8(_DRV2605_REG_MODE, 0x00)  # out of standby
        self._write_u8(_DRV2605_REG_RTPIN, 0x00)  # no real-time-playback

        self._write_u8(_DRV2605_REG_WAVESEQ1, 1)  # 1 = strong click 118 = programmatic buzz
        self._write_u8(_DRV2605_REG_WAVESEQ2, 0)
        self._write_u8(_DRV2605_REG_WAVESEQ3, 0)
        self._write_u8(_DRV2605_REG_WAVESEQ4, 0)
        self._write_u8(_DRV2605_REG_WAVESEQ5, 0)
        self._write_u8(_DRV2605_REG_WAVESEQ6, 0)
        self._write_u8(_DRV2605_REG_WAVESEQ7, 0)
        self._write_u8(_DRV2605_REG_WAVESEQ8, 0)
        
        self._write_u8(_DRV2605_REG_OVERDRIVE, 0) # only useful in open-loop mode, automatic in closed-loop
        self._write_u8(_DRV2605_REG_SUSTAINPOS, 0)
        self._write_u8(_DRV2605_REG_SUSTAINNEG, 0)
        self._write_u8(_DRV2605_REG_BREAK, 0)
        self._write_u8(_DRV2605_REG_AUDIOCTRL, 0x00)
        self._write_u8(_DRV2605_REG_AUDIOMINLV, 0x00)
        self._write_u8(_DRV2605_REG_AUDIOMAXLV, 0x00)
        self._write_u8(_DRV2605_REG_AUDIOMINDR, 0x00)
        self._write_u8(_DRV2605_REG_AUDIOMAXDR, 0x00)

        loc = 'init'
        self.log(loc)
        self.check(loc)

        #AUTO_CAL
        #self._write_u8(_DRV2605_REG_MODE, 0x07)
        self.autocal()

        # LRA MODE
        self.use_LRA()
        self.library = LIBRARY_LRA

        # control1 = self._read_u8(_DRV2605_REG_CONTROL1)
        # control2 = self._read_u8(_DRV2605_REG_CONTROL2)
        # control3 = self._read_u8(_DRV2605_REG_CONTROL3)
        # control4 = self._read_u8(_DRV2605_REG_CONTROL4)
        # control5 = self._read_u8(_DRV2605_REG_CONTROL5)

        self._write_u8(_DRV2605_REG_CONTROL2, 0xF5)#01110101 closed loop unidirectional
        # set default to internal trigger mode and LRA library.
        self._write_u8(_DRV2605_REG_MODE, 0x40) #put into STANDBY
        # self.mode = MODE_INTTRIG
        # self.library = LIBRARY_LRA
        
        self._sequence = _DRV2605_Sequence(self)


    def _read_u8(self, address):
        # Read an 8-bit unsigned value from the specified 8-bit address.
        with self._device as i2c:
            self._BUFFER[0] = address & 0xFF
            i2c.write_then_readinto(self._BUFFER, self._BUFFER, out_end=1, in_end=1)
        return self._BUFFER[0]

    def _write_u8(self, address, val):
        # Write an 8-bit unsigned value to the specified 8-bit address.
        with self._device as i2c:
            self._BUFFER[0] = address & 0xFF
            self._BUFFER[1] = val & 0xFF
            i2c.write(self._BUFFER, end=2)

    def check(self, loc):
        mylogs.info("_{}_".format(loc))
        # mylogs.debug("RATED: {}".format(self._read_u8(_DRV2605_REG_RATEDV)*0.02558))
        # mylogs.debug("CLAMP: {}".format(self._read_u8(_DRV2605_REG_CLAMPV)*0.02122))        
        mylogs.debug("VABTT: {}".format(self._read_u8(_DRV2605_REG_VBAT)*0.02196))
        mylogs.debug("RFREQ: {}".format(1/(self._read_u8(_DRV2605_REG_LRARESON)*0.09846)))

    def log(self, loc):
        control1 = self._read_u8(_DRV2605_REG_CONTROL1)
        control2 = self._read_u8(_DRV2605_REG_CONTROL2)
        control3 = self._read_u8(_DRV2605_REG_CONTROL3)
        control4 = self._read_u8(_DRV2605_REG_CONTROL4)
        control5 = self._read_u8(_DRV2605_REG_CONTROL5)        
        mylogs.info('_{}_\ncontrol1: {}\ncontrol2: {}\ncontrol3: {}\ncontrol4: {}\ncontrol5: {}'.format(loc,control1,control2,control3,control4,control5))

    def autocal(self):
        self.mode = MODE_AUTOCAL
        self.use_LRA()
        #self._write_u8(_DRV2605_REG_FEEDBACK, 0xAA)
        self._write_u8(_DRV2605_REG_RATEDV, 0x8C)#0x90)#0x83)#0x46)#0xB4)#0x12)#0x20) #0x12) # rated voltage (1.8V) !! CALCULATE ME !!
        self._write_u8(_DRV2605_REG_CLAMPV, 0XAA) #0x96)#0x57)#0xFA)#0x19)#0x23) #0x19)# overdrive v (2.5V)  !! CALCULATE ME !!
        mylogs.debug("RATED: {}".format(self._read_u8(_DRV2605_REG_RATEDV)*0.02558))
        mylogs.debug("CLAMP: {}".format(self._read_u8(_DRV2605_REG_CLAMPV)*0.02122))

        # control1 = self._read_u8(_DRV2605_REG_CONTROL1) #DRIVE_TIME: 21 = 0x15 = 100 10101
        # control2 = self._read_u8(_DRV2605_REG_CONTROL2)
        # control3 = self._read_u8(_DRV2605_REG_CONTROL3)
        # control4 = self._read_u8(_DRV2605_REG_CONTROL4)
        # control5 = self._read_u8(_DRV2605_REG_CONTROL5)

        #self._write_u8(_DRV2605_REG_CONTROL1, control1 ^ 0x06) #10010011 1001 0101 1001 0011
        #self._write_u8(_DRV2605_REG_CONTROL2, control2 & 0x75) #01100101 101
        #self._write_u8(_DRV2605_REG_CONTROL3, control3 ^ 0x28) #10101100 172 
        #self._write_u8(_DRV2605_REG_CONTROL4, control4 | 0x00) #

        self._write_u8(_DRV2605_REG_CONTROL1, 0x95)#0x90) 100 10101 DRIVE_TIME 2.1
        self._write_u8(_DRV2605_REG_CONTROL2, 0x00)#0xF5)#01110101 closed loop unidirectional
        #self._write_u8(_DRV2605_REG_CONTROL3, 0x20)
        #self._write_u8(_DRV2605_REG_CONTROL4, 0x30)
        #self._write_u8(_DRV2605_REG_CONTROL5, 0x30)
        
        #self._write_u8(_DRV2605_REG_MODE, 0x07)
        #elf._write_u8(_DRV2605_REG_GO, 0x01)
        self.play()

        loc = 'auto'
        self.log(loc)
        self.check(loc)
        
        i = 0
        while (self._read_u8(_DRV2605_REG_GO) & 0x01):
            self._read_u8(_DRV2605_REG_GO)
            if i==0:   
                mylogs.info("Not finished...")
                i = 1
        mylogs.info("GO REG: {}".format(self._read_u8(_DRV2605_REG_GO)))
        i = 0    
        #self._write_u8(_DRV2605_REG_GO, 0x00)
        #self.stop()
        self.diag()


    def play(self):
        """Play back the select effect(s) on the motor."""
        self._write_u8(_DRV2605_REG_GO, 1)

    def stop(self):
        """Stop vibrating the motor."""
        self._write_u8(_DRV2605_REG_GO, 0)

    def diag(self):
        """Check for auto calibration success"""
        diag = self._read_u8(_DRV2605_REG_STATUS)
        if (diag & 0x04):
            mylogs.error("Auto-calibration failed!")
            raise ValueError("Auto-calibration failed!")
        else:
            mylogs.info("Auto-calibration success!")
            #self.mode = MODE_INTTRIG
            #self.library = LIBRARY_LRA

    @property
    def mode(self):
        """
        The mode of the chip. Should be a value of:

          - MODE_INTTRIG: Internal triggering, vibrates as soon as you call play(). Default mode.
          - MODE_EXTTRIGEDGE: External triggering, edge mode.
          - MODE_EXTTRIGLVL: External triggering, level mode.
          - MODE_PWMANALOG: PWM/analog input mode.
          - MODE_AUDIOVIBE: Audio-to-vibration mode.
          - MODE_REALTIME: Real-time playback mode.
          - MODE_DIAGNOS: Diagnostics mode.
          - MODE_AUTOCAL: Auto-calibration mode.
          - MODE_STANDBY: Standby mode 0x40

        See the datasheet for the meaning of modes beyond MODE_INTTRIG.
        """
        return self._read_u8(_DRV2605_REG_MODE)

    @mode.setter
    def mode(self, val):
        if not 0 <= val <= 7:
            mylogs.warning("Mode must be a value within 0-7!")            
            raise ValueError("Mode must be a value within 0-7!")
        self._write_u8(_DRV2605_REG_MODE, val)

    @property
    def library(self):
        """
        The library selected for waveform playback.  Should be
        a value of:

        - LIBRARY_EMPTY: Empty
        - LIBRARY_TS2200A: TS2200 library A  (the default)
        - LIBRARY_TS2200B: TS2200 library B
        - LIBRARY_TS2200C: TS2200 library C
        - LIBRARY_TS2200D: TS2200 library D
        - LIBRARY_TS2200E: TS2200 library E
        - LIBRARY_LRA: LRA library

        See the datasheet for the meaning and description of effects in each
        library.
        """
        return self._read_u8(_DRV2605_REG_LIBRARY) & 0x07

    @library.setter
    def library(self, val):
        if not 0 <= val <= 6:
            mylogs.warning("Library must be a value within 0-6!")
            raise ValueError("Library must be a value within 0-6!")
        self._write_u8(_DRV2605_REG_LIBRARY, val)


    @property
    def sequence(self):
        """List-like sequence of waveform effects.
        Get or set an effect waveform for slot 0-6 by indexing the sequence
        property with the slot number. A slot must be set to either an Effect()
        or Pause() class. See the datasheet for a complete table of effect ID
        values and the associated waveform / effect.

        E.g. 'slot_0_effect = drv.sequence[0]', 'drv.sequence[0] = Effect(88)'
        """
        return self._sequence

    def set_waveform(self, effect_id, slot=0):
        """Select an effect waveform for the specified slot (default is slot 0,
        but up to 7 effects can be combined with slot values 0 to 6).  See the
        datasheet for a complete table of effect ID values and the associated
        waveform / effect.
        """
        if not 0 <= effect_id <= 123:
            mylogs.warning("Effect ID must be a value within 0-123!")
            raise ValueError("Effect ID must be a value within 0-123!")
        if not 0 <= slot <= 6:
            mylogs.warning("Slot must be a value within 0-6!")
            raise ValueError("Slot must be a value within 0-6!")
        self._write_u8(_DRV2605_REG_WAVESEQ1 + slot, effect_id)


    # pylint: disable=invalid-name
    def use_ERM(self):
        """Use an eccentric rotating mass motor (the default)."""
        feedback = self._read_u8(_DRV2605_REG_FEEDBACK)
        self._write_u8(_DRV2605_REG_FEEDBACK, feedback & 0x7F)

    # pylint: disable=invalid-name
    def use_LRA(self):
        """Use a linear resonance actuator motor."""
        feedback = self._read_u8(_DRV2605_REG_FEEDBACK)
        self._write_u8(_DRV2605_REG_FEEDBACK, feedback | 0x80)


class Effect:
    """DRV2605 waveform sequence effect."""

    def __init__(self, effect_id):
        self._effect_id = 0
        # pylint: disable=invalid-name
        self.id = effect_id

    @property
    def raw_value(self):
        """Raw effect ID."""
        return self._effect_id

    @property
    # pylint: disable=invalid-name
    def id(self):
        """Effect ID."""
        return self._effect_id

    @id.setter
    # pylint: disable=invalid-name
    def id(self, effect_id):
        """Set the effect ID."""
        if not 0 <= effect_id <= 123:
            mylogs.warning("Effect ID must be a value within 0-123!")
            raise ValueError("Effect ID must be a value within 0-123!")
        self._effect_id = effect_id

    def __repr__(self):
        return "{}({})".format(type(self).__qualname__, self.id)


class Pause:
    """DRV2605 waveform sequence timed delay."""

    def __init__(self, duration):
        # Bit 7 must be set for a slot to be interpreted as a delay
        self._duration = 0x80
        self.duration = duration

    @property
    def raw_value(self):
        """Raw pause duration."""
        return self._duration

    @property
    def duration(self):
        """Pause duration in seconds."""
        # Remove wait time flag bit and convert duration to seconds
        return (self._duration & 0x7F) / 100.0

    @duration.setter
    def duration(self, duration):
        """Sets the pause duration in seconds."""
        if not 0.0 <= duration <= 1.27:
            mylogs.warning("Pause duration must be a value within 0.0-1.27!")
            raise ValueError("Pause duration must be a value within 0.0-1.27!")
        # Add wait time flag bit and convert duration to centiseconds
        self._duration = 0x80 | round(duration * 100.0)

    def __repr__(self):
        return "{}({})".format(type(self).__qualname__, self.duration)


class _DRV2605_Sequence:
    """Class to enable List-like indexing of the waveform sequence slots."""

    def __init__(self, DRV2605_instance):
        self._drv2605 = DRV2605_instance

    def __setitem__(self, slot, effect):
        """Write an Effect or Pause to a slot."""
        if not 0 <= slot <= 6:
            mylogs.warning("Slot must be a value within 0-6!")
            raise IndexError("Slot must be a value within 0-6!")
        if not isinstance(effect, (Effect, Pause)):
            mylogs.warning("Effect must be either an Effect() or Pause()!")
            raise TypeError("Effect must be either an Effect() or Pause()!")
        # pylint: disable=protected-access
        self._drv2605._write_u8(_DRV2605_REG_WAVESEQ1 + slot, effect.raw_value)

    def __getitem__(self, slot):
        """Read an effect ID from a slot. Returns either a Pause or Effect class."""
        if not 0 <= slot <= 6:
            mylogs.warning("Slot must be a value within 0-6!")
            raise IndexError("Slot must be a value within 0-6!")
        # pylint: disable=protected-access
        slot_contents = self._drv2605._read_u8(_DRV2605_REG_WAVESEQ1 + slot)
        if slot_contents & 0x80:
            return Pause((slot_contents & 0x7F) / 100.0)
        return Effect(slot_contents)

    def __iter__(self):
        """Returns an iterator over the waveform sequence slots."""
        for slot in range(0, 7):
            yield self[slot]

    def __repr__(self):
        """Return a string representation of all slot's effects."""
        return repr(list(self))
