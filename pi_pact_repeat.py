import argparse
import pi_pact
import sys
import time
from typing import *

DEFAULT_ARGS = {'distance_increment': 0, 'wait_interval': 60}
OPTIONAL_ARGS = ['distance_increment', 'wait_interval']
REMOVE_ARGS = ['-dinc', '--distance_increment', '-wint', '--wait_interval', '-dfinal', '--distance_final',
               '-tfinal', '--timeout_final', 'niter', 'iterations']


def parse_args(args: List[str]) -> Dict[str, str]:
    """Input argument parser.

    Args:
        args (list): Input arguments as taken from sys.argv.

    Returns:
        Dictionary containing parsed input arguments. Keys are argument names.
    """
    parser = argparse.ArgumentParser(description="Script to run pi_pact.py repeatedly with variable"
                                                 "distance and interval increments")
    parser.add_argument('-dinc', '--distance_increment', type=float,
                        help='The change in distance between runs (m).')
    parser.add_argument('--distance', type=float, required=True,
                        help="Initial pre-measured distance between the devices (m).")
    parser.add_argument('--timeout', type=float, required=True,
                        help="Timeout (s) for both beacon advertiser and  scanner modes.")
    parser.add_argument('-wint', '--wait_interval', type=float,
                        help='The wait in between runs (s).')

    finish_group = parser.add_mutually_exclusive_group(required=True)
    finish_group.add_argument('-dfinal', '--distance_final', type=float,
                              help='The final distance to run pi_pact.py on.')
    finish_group.add_argument('-tfinal', '--timeout_final', type=int,
                              help='The total timeout for this script (s).')
    finish_group.add_argument('-niter', '--iterations', type=int,
                              help='The number of times to run pi_pact.py')

    # args from pi_pact.py
    mode_group = parser.add_mutually_exclusive_group(required=True)  # Note: means this script can be run as an
    # advertiser OR a scanner, but not both
    mode_group.add_argument('-a', '--advertiser', action='store_true',
                            help="Beacon advertiser mode.")
    mode_group.add_argument('-s', '--scanner', action='store_true',
                            help="Beacon scanner mode.")
    parser.add_argument('--config_yml', help="Configuration YAML.")
    parser.add_argument('--control_file', help="Control file.")
    parser.add_argument('--scan_prefix', help="Scan output file prefix.")
    parser.add_argument('--uuid', help="Beacon advertiser UUID.")
    parser.add_argument('--major', type=int,
                        help="Beacon advertiser major value.")
    parser.add_argument('--minor', type=int,
                        help="Beacon advertiser minor value.")
    parser.add_argument('--tx_power', type=int,
                        help="Beacon advertiser TX power.")
    parser.add_argument('--interval', type=int,
                        help="Beacon advertiser interval (ms).")
    parser.add_argument('--revist', type=int,
                        help="Beacon scanner revisit interval (s)")
    return vars(parser.parse_args(args))


def load_config(parsed_args: Dict[str, str]) -> Dict[str, str]:
    """Loads optional arguments into a config dict.

     Args:
        parsed_args (Namespace): Parsed input arguments.

    Returns:
        Configuration dictionary.
    """
    config = dict()
    config['distance'] = parsed_args.get('distance')
    print(parsed_args)

    for arg in OPTIONAL_ARGS:
        if parsed_args.get(arg):
            config[arg] = parsed_args.get(arg)
        else:
            config[arg] = DEFAULT_ARGS.get(arg)

    return config


def main(args: List[str]):
    """Repeatedly runs pi_pact.py with variable distance and interval increments.

    Args:
        args (list): Arguments as provided by sys.argv.

    Raises:
        ValueError: Distance increment must allow final distance to be reached.
    """
    parsed_args: dict = parse_args(args)
    config: dict = load_config(parsed_args)
    distance: float = config.get('distance')
    arg_list: List[str] = args
    for arg in REMOVE_ARGS:
        if arg in arg_list:
            del arg_list[arg_list.index(arg) + 1]
            arg_list.remove(arg)
    arg_list[args.index('--distance') + 1] = str(distance)

    if parsed_args.get('distance_final'):
        if (distance - parsed_args.get('distance_final')) / config.get('distance_increment') < 0:
            while (distance - parsed_args.get('distance_final')) / config.get('distance_increment') < 0:
                pi_pact.main(arg_list)
                distance -= config.get('distance_increment')
                arg_list[args.index('--distance') + 1] = str(distance)
                time.sleep(config.get('wait_interval'))
        else:
            raise ValueError("Distance increment must allow final distance to be reached.")
    elif parsed_args.get('timeout_final'):
        start_time: float = time.monotonic()
        while (time.monotonic() - start_time) < parsed_args.get('distance_final'):
            pi_pact.main(arg_list)
            distance -= config.get('distance_increment')
            arg_list[args.index('--distance') + 1] = str(distance)
            time.sleep(config.get('wait_interval'))
    else:
        for i in range(parsed_args.get('iterations')):
            pi_pact.main(arg_list)
            distance -= config.get('distance_increment')
            arg_list[args.index('--distance') + 1] = str(distance)
            time.sleep(config.get('wait_interval'))


if __name__ == '__main__':
    """Script execution."""
    main(sys.argv[1:])
