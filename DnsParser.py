import os
from dnszone import dnszone
from blackhc.progress_bar import with_progress_bar
from logzero import logger


class DnsParser:
    def __init__(self, ip, filename=None, debug=False):

        self.ip = ip
        self.filename = filename
        self.debug = debug
        self.results = []
        self.names = None
        self.zonefile = None
        if self.filename is None:
            raise DnsParserInputError("filename", "Must include filename to parse")

    def get_domain_from_file(self):
        if self.filename is None:
            return False
        domain, ext = os.path.splitext(self.filename)
        return domain

    def parse_zonefile(self):
        self.zonefile = dnszone.zone_from_file(
            self.get_domain_from_file(), self.filename
        )
        self.names = list(self.zonefile.names)
        return True

    def check_ip(self, name):
        try:
            ips = self.zonefile.names[name].records("A").items
        except AttributeError as e:
            if self.debug:
                logger.info("Skipping %s: %s" % (name, e))
            return
        if self.ip in ips:
            if self.debug:
                logger.info("!!! IP %s in %s for %s" % (self.ip, ips, name))
            self.results.append(name)

    def run_parser(self):
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
    def __init__(self, expression, message):
        """Exception raised for errors in the input.

		Attributes:
			expression -- input expression in which the error occurred
			message -- explanation of the error
		"""
        self.expression = expression
        self.message = message
