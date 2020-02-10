# DNS Parser

Parses BIND9 files to look for records pointing to an IP.

## Installation

Clone the repo, then use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
git clone https://github.com/javiergayala/DNSParser.git
python -m pip install -r requirements.txt
```

## Usage

```bash
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
  --version             show program's version number and exit
```

### `-f` usage

When using `-f` you can either specify a specific file, **OR** you can specify a directory name (such as `./`) and the script will compile a list of files that conform to the following filename standard:

`domain.com.zone`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
