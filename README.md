# APLocator

Script created at i2t. It retrieves the location from a gps device, runs 2 commands and saves the results.

Runs on Ubuntu 20.04 LTS (tested on Kubuntu).

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

Setup permissions.

```
sudo adduser $USER dialout
```

Logout and login again.

## Configuration

Create a copy of `config.ini.sample` and rename it `config.ini`. Do not modify the original file.

```
cp config.ini.sample config.ini
```

Setup the gps and the output folder.

## How it works

1. Load the coordinates from a `LocationProvider`.
2. Run the command `nmcli dev wifi` using the package `pynmcli`.
3. Run the command `sudo iw dev wlp2s0 scan | egrep "on wlp2s0|signal:|SSID:" | sed -e "s/\tsignal: //" -e "s/\tSSID: //" -e "s/BSS //" -e "s/associated//" -e "s/ -- //" | awk '{ORS = (NR % 3 == 0)? "\n" : " "; print}' | sort` directly in the CLI.
4. Build a json object with the results.
5. Serialize the json object and save it to a file.

## Run

From the terminal, run `python3 src/run.py some_identifier`
