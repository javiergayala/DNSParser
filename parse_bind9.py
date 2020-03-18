#!/usr/bin/env python3
"""Read in and parse BIND9 Zone Files."""

__author__ = "Javier Ayala"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import ipaddress
import logging
import os

import logzero
from blackhc.progress_bar import with_progress_bar
from dnszone import dnszone
from logzero import logger

from DnsParser import DnsParser, DnsParserError, DnsParserInputError
from ScriptGenerator import ScriptGenerator

# Read in the zone file
zonefile = None
ip = ""
# Debug
debugOn = False
# Initialize the results holder
victims = []


def parseIp(ip=None):
    if not ip:
        logger.error("NO IP ADDRESS PROVIDED TO parseIp()")
        return None
    try:
        parsedIp = ipaddress.ip_address(ip)
    except ValueError as e:
        logger.error("Error Parsing IP: %s" % e)
        logger.error("Provided IP is not a valid IP: %s" % ip)
        return None
    return parsedIp


def main(args):
    """Enter the app."""
    global victims
    logzero.loglevel(logging.INFO)
    if args.verbose >= 1:
        logzero.loglevel(logging.DEBUG)
    logger.debug(args)
    parsedip = parseIp(ip=args.ip)
    if not parsedip:
        cname = args.ip
    record_type = "A"
    if args.aaaa:
        record_type = "AAAA"
        logger.info("Record Type set to AAAA")
    if args.filenames:
        filenames = filenamesToList(args.filenames, args.file_ext)
        logger.debug("Filename(s) parsing: %s" % filenames)
    for filename in filenames:
        dnsp = DnsParser(
            parsedip,
            filename=filename,
            record_type=record_type,
            debug=args.debug,
            scriptOutType=args.scriptouttype,
        )
        tmpresults = dnsp.run_parser()
        if tmpresults:
            victims.extend(tmpresults[:])
    if not args.scriptouttype:
        logger.info("Results of run:")
        print(*victims, sep="\n")
    else:
        if parsedip:
            scriptoutput = ScriptGenerator(
                records=victims, ip=parsedip.exploded, action=args.scriptouttype
            )
        elif cname:
            scriptoutput = ScriptGenerator(
                records=victims, cname=cname, action=args.scriptouttype
            )
        # print("%s" % scriptoutput.get_script())
        print(*scriptoutput.get_script(), sep="\n")


def filenamesToList(filenames, file_ext):
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
            if ext == file_ext:
                found_files.append(os.path.join(tmpfilenames[0], entry))
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

    # Option argument for IPv6 which defaults to False

    parser.add_argument(
        "-6",
        "--IPv6",
        "--AAAA",
        action="store_true",
        dest="aaaa",
        default=False,
        help="Perform a search for a 'AAAA' record",
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

    parser.add_argument(
        "-e",
        "--ext",
        action="store",
        dest="file_ext",
        default=".zone",
        help="Filename Extension to target (Defaults to .zone)",
    )

    parser.add_argument(
        "-o",
        "--output-as-script-type",
        action="store",
        dest="scriptouttype",
        help="Produce output that can be used in a DNS script. Must include type (del, add)",
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
