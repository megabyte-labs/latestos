## Usage

Open your terminal and run:

```sh
latestos <os_name> <json_filename> <bash_command>
```

**NOTE:** The last argument is optional.

## Examples

```sh
latestos fedora template.json
```

```sh
latestos arch ./mydir/template.json
```

```sh
latestos ubuntu template.json ls .
```

## Options

This CLI currently checks the following options/distros:

- arch
- ubuntu
- fedora
- centos
- debian
- raspbian
- windows insiders preview

**Windows Insiders Preview**

If you're interested in extracting the latest OS version for Windows Insiders Preview, you'll need to:

1. Install Firefox
2. Download and extract the corresponding [geckodriver](https://github.com/mozilla/geckodriver/releases)
3. Make sure it's executable. If it is not, just run: ```chmod +x geckodriver```
4. Add it to your `PATH` or any location on system's `PATH`
