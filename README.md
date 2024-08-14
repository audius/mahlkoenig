# Mahlkönig API client

Helper scripts to interact with the Mahlkönig API. The CLI allows one to perform tasks on the API
without using the web interface.

The development of this client was kindly supported by [Hemro International AG](https://www.mahlkoenig.com).
This module is an official product and the development happens independently. API breaking may happen at
any given time.

## Installation

The package is available in the [Python Package Index](https://pypi.org/project/audiness/).

## Setup

It's required to set up your user upfront using the API client. Use the admin
interface or mobile app to register yourself.

## Usage

Use `--help` to get a general overview or `COMMAND --help` for the detailed help.

```bash
$ mahlkoenig --help

```

If you don't want to enter the username, the password and the URL then put them in the
environment of your shell.

```bash
$ export USERNAME="your.username@example.com"
$ export PASSWORD="your_password"
$ export URL="https://mahlkoenig.com/"
```

or create a Nix shell (see `default.nix` for details).

## License

`mahlkoenig` is licensed under MIT, for more details check the LICENSE file.
