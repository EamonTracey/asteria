from dataclasses import dataclass

from base.component import Component
from air.mcp9808 import MCP9808State


@dataclass
class TemperatureRegulationState:
    ...


class TemperatureRegulationComponent(Component):

    def __init__(self, mcp9808_state: MCP9808State):
        self._state = TemperatureRegulationState()

        self._mcp9808_state = mcp9808_state

    @property
    def state(self):
        return self._state

    def dispatch(self):
        # TODO: regulate temperature with heaters
        ...
