import serial, time
from HPS_h import *

class HPS:
    def __init__(self, port, baudrate = 19200, bytesize = serial.EIGHTBITS, parity = serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE):
        self.port = port
        self.baudrate = baudrate
        self.s = serial.Serial( port, baudrate = baudrate, bytesize = bytesize, parity = parity, stopbits = stopbits, timeout = 2, xonxoff=0, rtscts=0)
        self.message_read = ''
        self.message_written = ''

    def HPSCommand(self, slave, command):
        self.StartMessage()
        self.AddByte( 0x24 ) # Address notification
        self.AddByte( slave )
        self.AddCommand( command )
        self.EndMessage()
        self.WriteMessage()
        message  = self.ReadMessage()
        return message

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


    def AddCommand(self, command):
        self.message_written = self.message_written + command

    def EndMessage(self):
        self.message_written = self.message_written + chr( 0x0D )

    def WriteMessage(self):
        self.s.write( self.message_written )

    def ReadMessage(self):
        self.message_read = self.s.readline( )
        return self.message_read
