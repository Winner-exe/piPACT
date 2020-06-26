import argparse
import pi_pact
import sys
import time
from typing import *

DEFAULT_ARGS = {'-dinc': 0, '-wint': 60}
OPTIONAL_ARGS = ['-dinc', '-wint']


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
    parser.add_argument('--timeout', type=float, required=True
    help = "Timeout (s) for both beacon advertiser and  scanner modes.")
    parser.add_argument('-wint', '--wait_interval', type=float,
                        help='The wait in between runs (s).')

    finish_group = parser.add_mutually_exclusive_group(required=True)
    finish_group.add_argument('-dfinal', '--distance_final', type=float,
                              help='The final distance to run pi_pact.py on.')
    finish_group.add_argument('-tfinal', '--timeout_final', type=int,
                              help='The total timeout for this script (s).')
    finish_group.add_argument('-niter', '--iterations', type=int,
                              help='The number of times to run pi_pact.py')
    return vars(parser.parse_args(args))


def load_config(parsed_args: Dict[str, str]) -> Dict[str, str]:
    """Loads optional arguments into a config dict.

     Args:
        parsed_args (Namespace): Parsed input arguments.

    Returns:
        Configuration dictionary.
    """
    config = dict()
    config['--distance'] = parsed_args['--distance']

    for arg in OPTIONAL_ARGS:
        if parsed_args[arg]:
            config[arg] = parsed_args[arg]
        else:
            config[arg] = DEFAULT_ARGS[arg]

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
    distance: float = config['--distance']
    arg_list: List[str] = args
    arg_list[args.index('--distance') + 1] = str(distance)

    if parsed_args['-dfinal']:
        if (distance - parsed_args['-dfinal']) / config['-dinc'] < 0:
            while (distance - parsed_args['-dfinal']) / config['-dinc'] < 0:
                pi_pact.main(arg_list)
                distance -= config['-dinc']
                arg_list[args.index('--distance') + 1] = str(distance)
                time.sleep(config['-wint'])
        else:
            raise ValueError("Distance increment must allow final distance to be reached.")
    elif parsed_args['-tfinal']:
        start_time: float = time.monotonic()
        while (time.monotonic() - start_time) < parsed_args['-dfinal']:
            pi_pact.main(arg_list)
            distance -= config['-dinc']
            arg_list[args.index('--distance') + 1] = str(distance)
            time.sleep(config['-wint'])
    else:
        for i in range(parsed_args['-niter']):
            pi_pact.main(arg_list)
            distance -= config['-dinc']
            arg_list[args.index('--distance') + 1] = str(distance)
            time.sleep(config['-wint'])


if __name__ == '__main__':
    """Script execution."""
    main(sys.argv[1:])
