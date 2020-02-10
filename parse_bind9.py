#!/usr/bin/env python3
"""Read in and parse BIND9 Zone Files."""

__author__ = "Javier Ayala"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import os

from blackhc.progress_bar import with_progress_bar
from dnszone import dnszone
from DnsParser import DnsParser
from DnsParser import DnsParserError
from DnsParser import DnsParserInputError

from logzero import logger

# Read in the zone file
zonefile = dnszone.zone_from_file(
    "rackspace.com", "/Users/jayala/tmp/rackspace.com.zone"
)
ip = "23.253.6.64"
# Debug
debugOn = False
# Initialize the results holder
victims = []


def main(args):
    """ Main entry point of the app """
    global victims
    logger.info("hello world")
    logger.info(args)
    if args.filenames:
        filenames = filenamesToList(args.filenames)
        logger.info(filenames)
    for filename in filenames:
        dnsp = DnsParser(args.ip, filename=filename, debug=args.debug)
        tmpresults = dnsp.run_parser()
        if tmpresults:
            victims.extend(tmpresults[:])
    print("Results of run:")
    print(*victims, sep="\n")


def filenamesToList(filenames):
    """Split the filenames into a list.

    Arguments:
        filenames {string} -- comma-separated list of filenames

    Returns:
        [type] -- [description]
    """
    tmpfilenames = filenames.split(",")
    if os.path.isdir(tmpfilenames[0]):
        found_files = []
        for entry in os.listdir(tmpfilenames[0]):
            name, ext = os.path.splitext(entry)
            if ext == ".zone":
                found_files.append(entry)
        tmpfilenames = found_files

    return tmpfilenames


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("ip", help="IP Address to target in your search")

    # Optional argument flag which defaults to False
    parser.add_argument(
        "-d", "--debug", action="store_true", default=False, help="Enable debug mode"
    )

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument(
        "-f",
        "--filenames",
        action="store",
        dest="filenames",
        required=True,
        help="Filename(s) to parse (BIND9 Format). Optionally provide a single directory name to parse for filenames ending in '.zone'.",
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
