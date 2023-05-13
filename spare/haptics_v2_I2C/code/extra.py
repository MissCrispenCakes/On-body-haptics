        
        #self._write_u8(_DRV2605_REG_AUDIOMAX, 0x64)
        #self._write_u8(_DRV2605_REG_AUTOCALCOMP, 1) # = const(0x18)
        #self._write_u8(_DRV2605_REG_AUTOCALEMP, 1) # = const(0x19)        
        #self._write_u8(_DRV2605_REG_FEEDBACK, 1) # = const(0x1A)

        # G0832012 LRA
        # rated voltage: 1.8 VrmsAC Sine
        # input frequency: 235 Hz
        # axis of vibration: Z (perp to surface -> parallel to user skin -> vibration toward user)

        self._write_u8(_DRV2605_REG_MODE, 0x07)  # into auto-cal
        self.mode = MODE_AUTOCAL # auto-cal
        self._write_u8(_DRV2605_REG_RATEDV, 0x12) # rated voltage (1.8V) !! CALCULATE ME !!
        self._write_u8(_DRV2605_REG_CLAMPV, 0x19) # overdrive v (2.5V)  !! CALCULATE ME !!
 
        # want LRA closed loop instead
        # need to auto-control resonant frequency
        # maybe change DRIVE_TIME  !! CALCULATE ME !! 
        # 1/235 hz => *10E3 = 42.55ms => *.5 = 21.3 ms | 0x15
        # default: 1X0 10011
        #         ^000 00110  
        # want:    1X0 10101
        control1 = self._read_u8(_DRV2605_REG_CONTROL1)
        self._write_u8(_DRV2605_REG_CONTROL1, control1 ^ 0x06)

        # maybe need to change LRA auto-resonance SAMPLE_TIME => default is 300 us
        # 11 11 0101; 250us = 11 10 0101 = E5; 200us = 11 01 0101 = D5; 150us = 11 00 0101 = C5
        #&11 10 0101
        # 11 10 0101
        #control2 = self._read_u8(_DRV2605_REG_CONTROL2)
        #self._write_u8(_DRV2605_REG_CONTROL2, control2 & 0xE5)

        # want LRA closed-loop default
        # also maybe set LRA DRIVE MODE to twice per cycle => default is once per cycle
        # set default thresh, closed-loop, default comp, default format, LRA twice cycle, default analog, default auto
        # 10 1 0 0 0 0 0
        #^00 1 0 0 1 0 0 
        # 10 0 0 0 1 0 0
        control3 = self._read_u8(_DRV2605_REG_CONTROL3)
        self._write_u8(_DRV2605_REG_CONTROL3, control3 ^ 0x24)

        # maybe need to change auto calibration time => default 500ms - 700ms
        # !!!!
        # BE CAREFUL WITH CONTROL 4 AS IT HAS A _ONE TIME PROGRAM_ BIT => CANNOT REVERSE!!!!
        # !!!!
        #control4 = self._read_u8(_DRV2605_REG_CONTROL4) 
        #self._write_u8(_DRV2605_REG_CONTROL4, control4 | XxXX )

        #self.autocal()               