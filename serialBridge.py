import serial
import time
from sys import platform
import serial.tools.list_ports as port_list

class SerialBridge:

    async def open_bridge(self):

        # Open grbl serial port        
        if platform == "linux" or platform == "linux2":
            self.s = self.connect_to_ports_linux()

        elif platform == "darwin":  ##OS X
            raise Exception( "Not Mac compatible yet" )
            
        elif platform == "win32":
            self.s = self.connect_to_ports()
            
        if self.s is None:   return

        # Wake up grbl
        self.s.write(b"\r\n\r\n")
        time.sleep(2)   # Wait for grbl to initialize
        self.s.flushInput()  # Flush startup text in serial input

    async def stream_g_code_file(self, filename= 'grbl.code'):
        # Stream g-code to grbl
        f = open(filename, 'r')
        for line in f:
            await self.send_command(line)

    async def send_command(self, command) -> bytes:

        if self.s is None: return

        l = command.strip()  # Strip all EOL characters for consistency
        print('Sending: ' + l)
        payload = l + '\n'
        q = bytes(payload, encoding='utf-8')
        self.s.write(q)  # Send g-code block to grbl
        grbl_out = self.s.readline()  # Wait for grbl response with carriage return
        print("response: \n")
        print(grbl_out.strip())
        return grbl_out.strip()

    async def goto(self, x: float, y: float, z: float, sys: int):
        if sys == 1:
            await self.send_command("G91")
        if sys == 0:
            await self.send_command("G90")
              
        command = "G0 x " + str(x) + " y " + str(y) + " z " + str(z)
        
        await self.send_command(command)

    
    def connect_to_ports(self) -> serial.Serial:

        #####        
        ard=None
        all_ports = list(port_list.comports())
        pos_ports = [p.device for p in all_ports  if "CH340" in p.description]
       
        if len(pos_ports)==0:       print("No Port Found"); ## You may wish to cause an error here.   
        ## Search for Suitable Port
        for port in pos_ports: 
            try:      
                ard = serial.Serial(port, 115200, timeout=0.1)
                print("Connecting to port"+ port)
            except:   
                continue
        return ard

    def connect_to_ports_linux(self) -> serial.Serial:
        #Not tested yet, and it asumes that the port is the first one in the list
        all_ports = list(port_list.comports())
        port = all_ports[0].device
        try:
            ard = serial.Serial(port, 115200, timeout=0.1, write_timeout=0.1, inter_byte_timeout=0.1)
        except:
            print("Linux: port connection failed")
            return None
        return ard



    
