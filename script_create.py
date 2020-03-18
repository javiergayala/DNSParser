#!/usr/bin/env python3
"""
Create a script to use with the DNS Manager
"""

__author__ = "Javier Ayala"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import ipaddress
import itertools
import logging
import os

import logzero
import tldextract
from blackhc.progress_bar import with_progress_bar
from logzero import logger

from DnsRecord import DnsRecord
from parse_bind9 import parseIp
from ScriptGenerator import ScriptGenerator


def main(args):
    """Engine of the script."""
    logzero.loglevel(logging.INFO)
    if args.verbose >= 1:
        logzero.loglevel(logging.DEBUG)
    logger.debug(args)
    parsedip = parseIp(ip=args.ip)
    records_flat = list(itertools.chain(*args.records))
    parsedRecords = []
    for record in records_flat:
        logger.debug("Parsing Record: %s" % record)
        r = tldextract.extract(record)
        parsedRecords.append(DnsRecord(domain=r.registered_domain, entry=r.fqdn))
    if parsedip:
        logger.debug("Parsed IP: %s" % parsedip)
        scriptoutput = ScriptGenerator(
            records=parsedRecords, ip=parsedip.exploded, action=args.scriptouttype
        )
    else:
        cname = args.ip
        logger.debug("CNAME: %s" % args.ip)
        scriptoutput = ScriptGenerator(
            records=parsedRecords, cname=cname, action=args.scriptouttype
        )
    print(*scriptoutput.get_script(), sep="\n")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument for the IP address
    parser.add_argument("ip", help="IP Address to target in the script")

    # Required argument flag to specify the hostnames
    parser.add_argument(
        "-r",
        "--record",
        action="append",
        nargs="+",
        dest="records",
        help="Hostname entries to use when creating the script (invoke one time PER hostname)",
    )

    # Required argument flag to determine the script output type
    parser.add_argument(
        "-o",
        "--output-as-script-type",
        action="store",
        dest="scriptouttype",
        help="Produce output that can be used in a DNS script. Must include type (del, add)",
    )

    # Optional argument flag which defaults to False
    parser.add_argument(
        "-d", "--debug", action="store_true", default=False, help="Enable debug mode"
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
