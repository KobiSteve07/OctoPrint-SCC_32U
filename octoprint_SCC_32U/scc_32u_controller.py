import serial
import time
import serial.tools.list_ports

class Scc32uController:
    def __init__(self, port=None, baud_rate=9600):
        self.port = port or self.auto_detect_port()
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
        self.slider_values = [1500] * 6  # Default values for 6 servos

    def auto_detect_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "USB" in port.description:
                return port.device
        raise Exception("Could not auto-detect a suitable serial port.")

    def send_command(self, command):
        command += '\r'  # Append carriage return for the SSC-32
        self.ser.write(command.encode())
        time.sleep(0.1)  # Wait for the command to execute

    def move_arm(self, servo_id, position):
        if 0 <= servo_id < len(self.slider_values):
            self.slider_values[servo_id] = position
            time_to_move = 1000  # Time to move in milliseconds
            command = f"#{servo_id} P{position} T{time_to_move}"
            self.send_command(command)

    def batch_update(self):
        for servo_id, position in enumerate(self.slider_values):
            time_to_move = 1000  # Time to move in milliseconds
            command = f"#{servo_id} P{position} T{time_to_move}"
            self.send_command(command)

    def close(self):
        self.ser.close()
