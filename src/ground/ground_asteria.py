import board
import busio
import digitalio

from base.loop import Loop
from ground.command import CommandComponent


class GroundAsteria:

    def __init__(self, command_port: int):
        self._loop = Loop(1)

        # Connect to the SPI bus.
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # Command.
        command_component = CommandComponent(command_port)
        command_state = command_component.state
        self._loop.add_component(command_component, 1)

        # Ground RFM95W.
        ground_rfm95w_component = GroundRFM95WComponent(
            spi, board.D5, board.D6, command_state)
        self._loop.add_component(ground_rfm95w_component, 1)

    def run(self, steps: int):
        self._loop.run(steps)
