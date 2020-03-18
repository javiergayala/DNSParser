# DNS Parser

Parses BIND9 files to look for records pointing to an IP.

## Installation

Clone the repo, then use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
git clone https://github.com/javiergayala/DNSParser.git
python -m pip install -r requirements.txt
```

## Usage (`parse_bind9.py`)

Parses a Bind9 Zone file looking for entries that match a specified IP address.

```text
usage: parse_bind9.py [-h] [-d] -f FILENAMES [-v] [--version] ip

positional arguments:
  ip                    IP Address to target in your search

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug mode
  -f FILENAMES, --filenames FILENAMES
                        Filename(s) to parse (BIND9 Format). Optionally
                        provide a single directory name to parse for filenames
                        ending in '.zone'.
  -v, --verbose         Verbosity (-v, -vv, etc)
  --version             show program version number and exit
```

### `-f` usage

When using `-f` you can either specify a specific file, **OR** you can specify a directory name (such as `./`) and the script will compile a list of files that conform to the following filename standard:

`domain.com.zone`

## Usage (`script_create.py`)

Given a list of records and an IP/CNAME, creates output that can be pasted into the DNS Manager's script runner.

```text
usage: script_create.py [-h] [-r RECORDS [RECORDS ...]] [-o SCRIPTOUTTYPE]
                        [-d] [-v] [--version]
                        ip

positional arguments:
  ip                    IP Address to target in the script

optional arguments:
  -h, --help            show this help message and exit
  -r RECORDS [RECORDS ...], --record RECORDS [RECORDS ...]
                        Hostname entries to use when creating the script
                        (invoke one time PER hostname)
  -o SCRIPTOUTTYPE, --output-as-script-type SCRIPTOUTTYPE
                        Produce output that can be used in a DNS script. Must
                        include type (del, add)
  -d, --debug           Enable debug mode
  -v, --verbose         Verbosity (-v, -vv, etc)
  --version             show program version number and exit
```

### Example

```text
python script_create.py -r www.javierayala.co.id www.javier-ayala.asia -o add 192.168.0.2
[I 200318 11:06:34 ScriptGenerator:119] DnsRecord(domain='javierayala.co.id', entry='www.javierayala.co.id')
[I 200318 11:06:34 ScriptGenerator:119] DnsRecord(domain='javier-ayala.asia', entry='www.javier-ayala.asia')

=============================
Output for the script runner:
=============================

add_address_record javierayala.co.id www.javierayala.co.id 192.168.0.2
add_address_record javier-ayala.asia www.javier-ayala.asia 192.168.0.2
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
