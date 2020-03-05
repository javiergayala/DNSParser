"""Parse a DNS file for particular records.

Raises:
    DnsParserInputError: Exception for errors pertaining to the input recevied.

Returns:
    [list] -- Records resulting from the search.
"""
import ipaddress
import logging
import os

import logzero
from blackhc.progress_bar import with_progress_bar
from dnszone import dnszone
from logzero import logger
from DnsRecord import DnsRecord


class DnsParser:
    """Parse a DNS file for particular records.

    Raises:
        DnsParserInputError: Exception for errors pertaining to the input recevied.

    Returns:
        [list] -- Records resulting from the search.
    """

    def __init__(
        self, ip, filename=None, record_type="A", debug=False, scriptOutType=None
    ):
        """Initialize the class.

        Arguments:
            ip {string} -- IP address serving the basis of the search.

        Keyword Arguments:
            filename {str} -- Path to the BIND9 zone file (default: {None})
            record_type {str} -- Type of record to search for (default: {"A"})
            debug {bool} -- Set to True to enable debug messages (default: {False})
            scriptOutType {str} -- Type of script to output (default: {None})

        Raises:
            DnsParserInputError: Exception for errors pertaining to the input recevied.
        """
        self.ip = ip
        self.filename = filename
        self.debug = debug
        self.scriptOutType = scriptOutType
        self.results = []
        self.domain = None
        self.names = None
        self.zonefile = None
        self.record_type = "A" if self.ip.version == 4 else "AAAA"
        logzero.loglevel(logging.INFO)
        if self.debug:
            logzero.loglevel(logging.DEBUG)
        if self.filename is None:
            raise DnsParserInputError("filename", "Must include filename to parse")

    def get_domain_from_file(self):
        """Extrapolate the domain name from the zone filename.

        Returns:
            {str} -- domain name
        """
        if self.filename is None:
            return False
        domain, ext = os.path.splitext(self.filename)
        return domain

    def parse_zonefile(self):
        """Parse the zonefile for the domain.

        Returns:
            {bool} -- True when parsed
        """
        logger.info("Domain name: %s" % self.get_domain_from_file())
        logger.info("Filename to open: %s" % self.filename)
        self.domain = self.get_domain_from_file()
        self.zonefile = dnszone.zone_from_file(self.domain, self.filename)
        self.names = list(self.zonefile.names)
        return True

    def check_ip(self, name):
        """Look for references of an IP within the zone file.

        Arguments:
            name {str} -- hostname to check against

        Keyword Arguments:
            record_type {str} -- Type of record to search for (default: {"A"})
        """
        try:
            ips = self.zonefile.names[name].records(self.record_type).items
        except AttributeError as e:
            if self.debug:
                logger.info("Skipping %s: %s" % (name, e))
            return
        if self.ip.version == 6:
            logger.debug("IPv6 Detected")
            exploded_ips = []
            for ip in ips:
                pIp = ipaddress.ip_address(ip)
                exploded_ips.append(pIp.exploded)
            ips = exploded_ips
        if self.ip.exploded in ips:
            if self.debug:
                logger.debug("!!! IP %s in %s for %s" % (self.ip.exploded, ips, name))
            if self.scriptOutType:
                rout = DnsRecord(domain=self.domain, entry=name)
                # rout = {"domain": self.domain, "entry": name}
                logger.debug("Individual result: %s" % rout)
                self.results.append(rout)
            else:
                self.results.append(name)

    def run_parser(self):
        """Initiate the check against the zone file.

        Returns:
            {list} -- list of matches
        """
        self.results = []
        if self.debug:
            logger.info("Getting zonefile info for: %s" % self.filename)
        if self.parse_zonefile():
            for name in with_progress_bar(self.names):
                self.check_ip(name=name)
                pass
            if self.debug:
                logger.info("Done!")
        if len(self.results) == 0:
            return None
        else:
            logger.debug("Results: %s" % self.results)
            return self.results

    def get_ip(self):
        """Return the IP Address used in the search.

        Returns:
            {string} -- IP Address used in the search.
        """
        return self.ip

    def get_results(self):
        """Return the results of the search.

        Returns:
            {list} -- List of strings containing the results.
        """
        return self.ip

    def __str__():
        return "ip: " + ip


class DnsParserError(Exception):
    """Base class exception for this module."""

    pass


class DnsParserInputError(DnsParserError):
    """Exception for errors pertaining to the input recevied."""

    def __init__(self, expression, message):
        """Exception raised for errors in the input.

        Attributes:
            expression -- input expression in which the error occurred
            message -- explanation of the error
        """
        self.expression = expression
        self.message = message
