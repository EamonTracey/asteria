import datetime
import logging
from typing import Optional

import click

from air.asteria import Asteria as AirAsteria
from ground.asteria import Asteria as GroundAsteria

logger = logging.getLogger(__name__)


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
    logger.info("Asteria Air.")
    logger.info("Developed by Sarah Kopfer, Nicholas Palma, and Eamon Tracey.")
    logger.info(f"{name=}")

    air_asteria = AirAsteria(name)
    air_asteria.run(0)


@asteria.command()
@click.argument("host", type=str)
@click.option("-n",
              "--name",
              type=str,
              default=None,
              help="The path to which to write the log file.")
@click.option("--port",
              type=int,
              default=9336,
              help="The UDP port on which to listen for commands.")
@click.option("--host_port",
              type=int,
              default=9340,
              help="The UDP port on which the host receives telemetry.")
def ground(host: str, name: Optional[str], port: int, host_port: int):
    """Run Asteria ground software."""

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
    logger.info("Asteria Ground.")
    logger.info("Developed by Sarah Kopfer, Nicholas Palma, and Eamon Tracey.")
    logger.info(f"{name=}")

    host = (host, host_port)
    ground_asteria = GroundAsteria(name, host, port)
    ground_asteria.run(0)


if __name__ == "__main__":
    asteria()
