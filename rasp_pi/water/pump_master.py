# relay_controller.py

import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017
from pump_config import PUMPS

class RelayController:
    def __init__(self, pump_map=PUMPS):
        self.pump_map = pump_map

        # Initialize I2C bus and MCP23017
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp = MCP23017(i2c)

        # Configure all pins as outputs and set to HIGH (relays off)
        for pin in pump_map.values():
            self.mcp.get_pin(pin).direction = 1  # Set as output (1)
            self.mcp.get_pin(pin).value = True   # Set HIGH (True) for active-LOW relays

    def activate(self, pump_name: str):
        pin = self.pump_map.get(pump_name)
        if pin is None:
            raise KeyError(f"Unknown pump: {pump_name}")
        self.mcp.get_pin(pin).value = False  # Set LOW (False) to activate relay
        print(f"→ {pump_name} ON")

    def deactivate(self, pump_name: str):
        pin = self.pump_map.get(pump_name)
        if pin is None:
            raise KeyError(f"Unknown pump: {pump_name}")
        self.mcp.get_pin(pin).value = True   # Set HIGH (True) to deactivate relay
        print(f"→ {pump_name} OFF")

    def cleanup(self):
        # Set all pins HIGH to ensure all relays are off
        for pin in self.pump_map.values():
            self.mcp.get_pin(pin).value = True
