# APLocator

Script created at i2t. It retrieves the location from a gps device, runs 2 commands and saves the results.

## Installation

Install python3-venv.

```
sudo apt-get install python3-venv
```

[Create and activate a Python virtual environment](https://docs.python.org/3/library/venv.html).

```
python3 -m venv /path/to/environment
cd /path/to/environment
source bin/activate
```

Install the dependencies. Do not use `sudo`.

```
pip3 install wheel pynmea2 pynmcli pyserial
```

## Configuration

Create a copy of `config.ini.sample` and rename it `config.ini`. Do not modify the original file.

```
cp config.ini.sample config.ini
```

Setup the gps and the output folder.