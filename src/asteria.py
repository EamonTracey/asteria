import datetime
import logging
import os
import sys
from typing import Optional

import click

DEFAULT_GROUND_PORT = 9336
DEFAULT_HOST_PORT = 9340

logger = logging.getLogger(__name__)


@click.group()
def asteria():
    """Asteria is an autonomously orienting lander.

    Authors: Sarah Kopfer, Nicholas Palma, Eamon Tracey"""


@asteria.command(context_settings={'show_default': True})
@click.option(
    "-n",
    "--name",
    type=str,
    default=None,
    help="The name of the program instance (corresponds to log file).")
@click.option("-d",
              "--directory",
              type=str,
              default=".",
              help="The working directory of the application.")
@click.option(
    "-p",
    "--proximity",
    type=float,
    default=50,
    help="The proximity from the ground at which flight 'begins' (ft).")
def air(name: Optional[str], proximity: int, directory: str):
    """Run Asteria flight software."""
    from air.asteria import Asteria as AirAsteria

    os.makedirs(directory, exist_ok=True)
    os.chdir(directory)

    # Naming is hard.
    if name is None:
        utc_date = datetime.datetime.now(datetime.timezone.utc)
        utc_date_string = utc_date.strftime("%Y%m%d%H%M%S")
        name = f"Asteria Air {utc_date_string}"

    # Initialize logging.
    logging.basicConfig(
        filename=f"{name}.log",
        format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
        datefmt="%Y%m%d%H%M%S",
        level=logging.INFO)
    logger.info("Asteria Air.")
    logger.info("Developed by Sarah Kopfer, Nicholas Palma, and Eamon Tracey.")
    logger.info(f"{name=}")

    air_asteria = AirAsteria(name, proximity)
    air_asteria.run(0)


@asteria.command(context_settings={'show_default': True})
@click.argument("host", type=str)
@click.option(
    "-n",
    "--name",
    type=str,
    default=None,
    help="The name of the program instance (corresponds to log file).")
@click.option("--port",
              type=int,
              default=DEFAULT_GROUND_PORT,
              help="The UDP port on which to listen for commands.")
@click.option("--host_port",
              type=int,
              default=DEFAULT_HOST_PORT,
              help="The UDP port on which the host receives telemetry.")
def ground(host: str, name: Optional[str], port: int, host_port: int):
    """Run Asteria ground software."""
    from ground.asteria import Asteria as GroundAsteria

    # Naming is hard.
    if name is None:
        utc_date = datetime.datetime.now(datetime.timezone.utc)
        utc_date_string = utc_date.strftime("%Y%m%d%H%M%S")
        name = f"Asteria Ground {utc_date_string}"

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


@asteria.command(context_settings={'show_default': True})
@click.argument("ground", type=str)
@click.option(
    "-n",
    "--name",
    type=str,
    default=None,
    help="The name of the program instance (corresponds to log file).")
@click.option("--port",
              type=int,
              default=DEFAULT_HOST_PORT,
              help="The UDP port on which to listen for telemetry.")
@click.option("--ground_port",
              type=int,
              default=DEFAULT_GROUND_PORT,
              help="The UDP port on which the ground receives commands.")
def host(ground: str, name: Optional[str], port: int, ground_port: int):
    """Run Asteria host software."""
    from PyQt5.QtWidgets import QApplication
    from host.asteria import Asteria as HostAsteria

    # Naming is hard.
    if name is None:
        utc_date = datetime.datetime.now(datetime.timezone.utc)
        utc_date_string = utc_date.strftime("%Y%m%d%H%M%S")
        name = f"Asteria Host {utc_date_string}"

    # Initialize logging.
    logging.basicConfig(
        filename=f"{name}.log",
        format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
        datefmt="%Y%m%d%H%M%S",
        level=logging.INFO)
    logger.info("Asteria Host.")
    logger.info("Developed by Sarah Kopfer, Nicholas Palma, and Eamon Tracey.")

    application = QApplication(sys.argv)
    ground = (ground, ground_port)
    host_asteria = HostAsteria(name, ground, port)
    host_asteria.run()
    application.exec_()


if __name__ == "__main__":
    asteria()
