# Asteria

Asteria is an autonomously orienting lander. The module descends under parachute and receives radio commands that determine the goal landing orientation. Prior to landing, the module deploys the appropriate landing gear for safe landing on diverse terrain.

Asteria consists of three primary components: air, ground, and host. The air component consists of the lander module that self-orients. The ground station includes three buttons to send radio commands and serves as a proxy between the air and the host. The host is any machine connected to the ground station to view real-time telemetry and also dispatch commands.

# Usage

To launch an Asteria flight, first clone the project repository and install the dependencies. A virtual environment is recommended. Note that many dependencies may be unnecessary to run the ground and host components.

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

The entrypoint to all components is `./run.sh`. Each internal command provides helpful information about execution and configuration through the `--help` flag.

```bash
Usage: asteria.py [OPTIONS] COMMAND [ARGS]...

  Asteria is an autonomously orienting lander.

  Authors: Sarah Kopfer, Nicholas Palma, Eamon Tracey

Options:
  --help  Show this message and exit.

Commands:
  air     Run Asteria flight software.
  ground  Run Asteria ground software.
  host    Run Asteria host software.
```
```bash
> ./run.sh air --help
Usage: asteria.py air [OPTIONS]

  Run Asteria flight software.

Options:
  -n, --name TEXT        The name of the program instance (corresponds to log
                         file).
  -d, --directory TEXT   The working directory of the application.  [default:
                         .]
  -p, --proximity FLOAT  The proximity from the ground at which flight
                         'begins' (ft).  [default: 50]
  --help                 Show this message and exit.
```
```bash
> ./run.sh ground --help
Usage: asteria.py ground [OPTIONS] HOST

  Run Asteria ground software.

Options:
  -n, --name TEXT      The name of the program instance (corresponds to log
                       file).
  --port INTEGER       The UDP port on which to listen for commands.
                       [default: 9336]
  --host_port INTEGER  The UDP port on which the host receives telemetry.
                       [default: 9340]
  --help               Show this message and exit.
```
```bash
> ./run.sh host --help
Usage: asteria.py host [OPTIONS] GROUND

  Run Asteria host software.

Options:
  -n, --name TEXT        The name of the program instance (corresponds to log
                         file).
  --port INTEGER         The UDP port on which to listen for telemetry.
                         [default: 9340]
  --ground_port INTEGER  The UDP port on which the ground receives commands.
                         [default: 9336]
  --help                 Show this message and exit.
```
