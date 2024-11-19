import datetime
import logging
from typing import Optional

import click

from air.asteria import Asteria as AirAsteria
from ground.asteria import Asteria as GroundAsteria


@click.group()
def asteria():
    """Asteria is an autonomously orienting lander.

    Authors: Sarah Kopfer, Nicholas Palma, Eamon Tracey"""


@asteria.command()
@click.option("-n",
              "--name",
              type=str,
              default=None,
              help="The path to which to write the log file.")
def air(name: Optional[str]):
    """Run Asteria flight software."""

    # Naming is hard.
    if name is None:
        utc_date = datetime.datetime.now(datetime.UTC)
        utc_date_string = utc_date.strftime("%Y%m%d%H%M%S")
        name = f"Asteria {utc_date_string}"

    # Initialize logging.
    logging.basicConfig(
        filename=f"{name}.log",
        format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
        datefmt="%Y%m%d%H%M%S",
        level=logging.INFO)
    logger.info("Asteria.")
    logger.info("Developed by Sarah Kopfer, Nicholas Palma, and Eamon Tracey.")
    logger.info(f"{name=}")

    air_asteria = AirAsteria(log_file)
    air_asteria.run(0)


@asteria.command()
@click.option("--command_port",
              type=int,
              default=9336,
              help="The UDP port on which to listen for commands.")
def ground(command_port: Optional[int]):
    """Run Asteria ground software."""

    ground_asteria = GroundAsteria(command_port)
    ground_asteria.run(0)


if __name__ == "__main__":
    asteria()
