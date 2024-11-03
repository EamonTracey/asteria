from typing import Optional

import click

from air.asteria import Asteria as AirAsteria
from ground.asteria import Asteria as GroundAsteria


@click.group()
def asteria():
    """Asteria is an autonomously orienting lander.

    Authors: Sarah Kopfer, Nicholas Palma, Eamon Tracey"""


@asteria.command()
@click.option("--log_file",
              type=str,
              default=None,
              help="The path to which to write the log file.")
def air(log_file: Optional[str]):
    air_asteria = AirAsteria()
    air_asteria.run(0)


@asteria.command()
@click.option("--command_port",
              type=int,
              default=9336,
              help="The UDP port on which to listen for commands.")
def ground(command_port: Optional[int]):
    ground_asteria = GroundAsteria(command_port)
    ground_asteria.run(0)


if __name__ == "__main__":
    asteria()
