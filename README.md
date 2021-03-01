<<<<<<< HEAD
# LatestOS

Latest OS version checker for Linux Distros using the Arizona Mirror

It currently checks the following distros:
- arch
- ubuntu
- fedora
- centos
- debian
- raspbian

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

**NOTE**
- The last argument is optional.

## Examples:
```sh
latestos fedora template.json
```

```sh
latestos arch ./mydir/template.json
```

```sh
latestos ubuntu template.json ls .
```
=======
# OS Version

Grabs the latest Linux distro version information from mirror.arizona.edu and injects it in a JSON file.
>>>>>>> 02e3f771e59e8684989edcbd81698a62a0d5ecac
