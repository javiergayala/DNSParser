import ipaddress
from logzero import logger


class ScriptGenerator:
    """Creates a script to use for the DNS Script Runner.

    Returns:
        {str} -- script to paste into the script runner
    """

    def __init__(self, records=[], ip=None, cname=None, action=None):
        """Initialize the ScriptGenerator class.

        Keyword Arguments:
            records {list} -- List of domains/hostnames to create a script for. (default: {[]})
            ip {ipaddress.IPv4Address or ipaddress.IPv6Address} -- IP Address (default: {None})
            cname {str} -- CNAME fqdn
            action {str} -- Action to take: del, add, etc. (default: {None})
        """
        self.records = records
        self.ip = ipaddress.ip_address(ip)
        self.cname = cname
        self.action = action
        self.actions = {
            "del_aaaa": "del_aaaa_record",
            "del_a": "del_address_record",
            "del_cname": "del_cname_record",
            "add_aaaa": "add_aaaa_record",
            "add_address": "add_address_record",
            "add_cname": "add_cname_record",
        }

    def add_a(self, record):
        """Produce a script entry for adding an A record.

        Arguments:
            record {dict} -- Dictionary of record to add

        Returns:
            {str} -- script entry
        """
        return f"add_address_record {record.domain} {record.entry.strip('.')} {self.ip}"

    def del_a(self, record):
        """Produce a script entry for deleting an A record.

        Arguments:
            record {dict} -- Dictionary of record to delete

        Returns:
            {str} -- script entry
        """
        return f"del_address_record {record.domain} {record.entry.strip('.')} {self.ip}"

    def add_aaaa(self, record):
        """Produce a script entry for adding a AAAA record.

        Arguments:
            record {dict} -- Dictionary of record to add

        Returns:
            {str} -- script entry
        """
        domain = record["domain"]
        return f"add_aaaa_record {record.domain} {record.entry.strip('.')} {self.ip}"

    def del_aaaa(self, record):
        """Produce a script entry for deleting a AAAA record.

        Arguments:
            record {dict} -- Dictionary of record to remove

        Returns:
            {str} -- script entry
        """
        return f"del_aaaa_record {record.domain} {record.entry.strip('.')} {self.ip}"

    def add_cname(self, record):
        """Produce a script entry for adding a CNAME record.

        Arguments:
            record {dict} -- Dictionary of record to add

        Returns:
            {str} -- script entry
        """
        return (
            f"add_cname_record {record.domain} {record.entry.strip('.')} {self.cname}"
        )

    def del_cname(self, record):
        """Produce a script entry for deleting a CNAME record.

        Arguments:
            record {dict} -- Dictionary of record to remove

        Returns:
            {str} -- script entry
        """
        return (
            f"del_cname_record {record.domain} {record.entry.strip('.')} {self.cname}"
        )

    def get_script(self):
        """Produce and return the script as a string.

        Returns:
            {str} -- Script output
        """
        script = []
        for record in self.records:
            logger.info(record)
            if self.ip:
                if self.ip.version == 4:
                    if self.action == "add":
                        script.append(self.add_a(record))
                    elif self.action == "del":
                        script.append(self.del_a(record))
                else:
                    if self.action == "add":
                        script.append(self.add_aaaa(record))
                    elif self.action == "del":
                        script.append(self.del_aaaa(record))
            elif self.cname:
                if self.action == "add":
                    script.append(self.add_cname(record))
                elif self.action == "del":
                    script.append(self.del_cname(record))
        return script

    def get_records(self):
        """Return the records provided to the class.

        Returns:
            {list} -- List of records
        """
        return self.records

    def get_ip(self):
        """Return the IP Address provided to the class.

        Returns:
            {ipaddress.IPv4Address or ipaddress.IPv6Address} -- IP Address
        """
        return self.ip

    def get_action(self):
        """Return the action representing the type of script to produce.

        Returns:
        {str} -- action as a string

        """
        return self.action

    def __str__():
        return "records: " + records + " , " + "ip: " + ip + " , " + "action: " + action
