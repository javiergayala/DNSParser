"""DNS Entry Data Class."""
import attr


@attr.s
class DnsRecord(object):
    """Data class representing a DNS Entry."""

    domain = attr.ib()
    entry = attr.ib()
