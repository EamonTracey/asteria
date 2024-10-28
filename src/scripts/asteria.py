import click

from air.air_asteria import AirAsteria
from ground.ground_asteria import GroundAsteria


@click.group()
def asteria():
    """Asteria is an autonomously orienting lander.

    Authors: Sarah Kopfer, Nicholas Palma, Eamon Tracey"""


@asteria.command()
def air():
    air_asteria = AirAsteria()
    air_asteria.run(0)


@asteria.command()
@click.option("--command_port",
              default=9336,
              help="The UDP port on which to listen for commands.")
def ground():
    ground_asteria = GroundAsteria()
    ground_asteria.run(0)


if __name__ == "__main__":
    asteria()
