# LatestOS

Latest OS version checker for Linux Distros using the Arizona Mirror

It currently checks the following distros:
- arch
- ubuntu
- fedora
- centos

## Installation
LatestOS requires [Python 3](https://www.python.org/downloads/) to run.

Install with pip:

```sh
pip install latestos
```

For UNIX-based systems with both Python 2 and Python 3 installed:

```sh
pip3 install latestos
```

## How to run?

Open your terminal and run:
```sh
latestos <os_name> <json_filename> <bash_command>
```

**NOTES**
- The last two arguments are optional.
- By default, json_filename is "template.json" and no bash command is passed. However... see next bulletpoint.
- Whenever you'll pass a bash command, you must also pass the json_filename.

## Examples:
```sh
latestos fedora
```

```sh
latestos arch ./mydir/template.json
```

```sh
latestos ubuntu template.json ls .
```
