# OS Version 

Grabs the latest OS version information for different operating systems and injects it in a JSON file.

It currently checks the following distros:
- arch
- ubuntu
- fedora
- centos
- debian
- raspbian
- windows insiders preview

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

** Windows Insiders Preview **
If you're interested in extracting the latest OS version for Windows Insiders Preview, you'll need to:
1. Install Firefox
2. Download and extract the corresponding geckodriver: https://github.com/mozilla/geckodriver/releases
3. Make sure it's executable. If it isn't, just run: ```chmod +x geckodriver```
4. Add it to your PATH or any location on system's PATH.

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
