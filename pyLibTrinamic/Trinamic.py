import serial, time
from Trinamic_h import *

class Trinamic:
    def __init__(self, port, baudrate = 19200, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE):
        self.s = serial.Serial( port, baudrate = baudrate, bytesize = bytesize, parity = parity, stopbits = stopbits, timeout = 2, xonxoff=0, rtscts=0)
        self.message_read = ''
        self.message_written = ''

    def instruction(self, address, command, motor=0, p1=0, p2=0, p3=0, p4=0, p5=0, p6=0 ):
        self.StartMessage()
        self.AddByte( address ) 
        self.AddByte( command )
        self.AddByte( motor )
        self.AddByte( p1 )
        self.AddByte( p2 )
        self.AddByte( p3 )
        self.AddByte( p4 )
        self.AddByte( p5 )
        self.AddByte( p6 )
        self.WriteMessage()

    def initialVelocity(self, motor, vstart, vmin, div, address=0):
        self.instruction()
        
    def acceleration(self, motor, acc, vmax, address=0):
        self.instruction()

    def setStepFreq(self, freq, address = 0):
        # Stop motors
        for i in range(1,6):
            self.constantRotation(i,0)
        self.instruction( address,
                          ord( STEP_FREQ),
                          self.lsB( freq )
                          )
                          
    def startRamp(self, motor, position, address = 0):
        if not self.validateMotor( motor ):
            return
        if not self.validateVelocity( position ):
            return
        self.instruction( address,
                          ord( START_RAMP),
                          motor,
                          self.lsB( position ),
                          self.msB( position )
                          )
                          
    def setTargetPosition(self, motor, position, address = 0):
        if not self.validateMotor( motor ):
            return
        if not self.validateVelocity( position ):
            return
        self.instruction( address,
                          ord( SET_TARGET_POSITION),
                          motor,
                          self.lsB( position ),
                          self.msB( position )
                          )
                          
    def setActualPosition(self, motor, position, address = 0):
        if not self.validateMotor( motor ):
            return
        if not self.validateVelocity( position ):
            return
        self.instruction( address,
                          ord( SET_ACTUAL_POSITION),
                          motor,
                          self.lsB( position ),
                          self.msB( position )
                          )
                          
    def constantRotation(self, motor, velocity, address = 0):
        if not self.validateMotor( motor ):
            return
        if not self.validateVelocity( velocity ):
            return
        self.instruction( address,
                          ord( SET_ROTATION_SPEED),
                          motor,
                          self.lsB( velocity ),
                          self.msB( velocity )
                          )
    def msB(self, value):
        if value < 0:
            return (65536+value) >> 8
        return value >> 8
        
    def lsB(self, value):
        if value < 0:
            low = (65536+value) & 255
        return value & 255
        
    def queryPositionActivity(self, motor, response_addr = 0, address = 0):
        if not self.validateMotor( motor ):
            return
        self.instruction( address,
                          ord( QUERY_PA),
                          motor,
                          response_addr )

        message  = self.ReadMessage()
        return message

    def getCurrentSpeed(self, motor, response_addr = 0, address = 0):
        if not self.validateMotor( motor ):
            return
        self.instruction( address,
                          ord( QUERY_SPEED),
                          motor,
                          response_addr )

        message  = self.ReadMessage()
        speed_loB = ord(message[3])
        speed_hiB = ord(message[4])
        return 8 * speed_hiB + speed_loB

    def StartMessage(self):
        self.message_written = ''


    def AddByte(self, data):
        data = int( data )
        if data > 255:
            high = data >> 8
            low = data & 255
            self.message_written = self.message_written + chr( high ) + chr( low )
        else:
            self.message_written = self.message_written + chr( data )

    def WriteMessage(self):
        self.tostr(self.message_written)
        #return
        self.s.write( self.message_written )

    def tostr(self, message):
        t = ''
        for i in message:
            t += str(ord(i)) + ' '
        print t

    def ReadMessage(self):
        self.message_read = self.s.read( BYTES )
        return self.message_read

    def  validateMotor(self, value):
        if value < MIN_MOTOR:
            print "Motor number "+str(value)+" below minimum value "+str(MIN_MOTOR)+"!"
            return False
        if value > MAX_MOTOR:
            print "Motor number "+str(value)+" above maximum value "+str(MAX_MOTOR)+"!"
            return False
        return True
    
    def  validateVelocity(self, value):
        if value < MIN_ROT_VEL:
            print "Motor velocity "+str(value)+" below minimum value "+str(MIN_ROT_VEL)+"!"
            return False
        if value > MAX_ROT_VEL:
            print "Motor velocity "+str(value)+" above maximum value "+str(MAX_ROT_VEL)+"!"
            return False
        return True
    
