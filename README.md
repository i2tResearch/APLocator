# APLocator

Script created at i2t. Retrieves the location from a gps device, runs 2 commands and saves the results.

Runs on Ubuntu 20.04 LTS (tested on Kubuntu).

## Installation

Install python3-venv.

```
sudo apt-get install python3-venv
```

[Create and activate a virtual environment](https://docs.python.org/3/library/venv.html).

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

Logout and login.

## Configuration

Create a copy of `config.ini.sample` and rename it `config.ini`. Do not modify the original file.

```
cp config.ini.sample config.ini
```

Open the file and setup the gps and the output folder.

## How it works

1. Loads the coordinates from a `LocationProvider`.
2. Runs the command `nmcli dev wifi` using the package `pynmcli`. Try it on a terminal!
3. Runs the command `sudo iw dev wlp2s0 scan | egrep "on wlp2s0|signal:|SSID:" | sed -e "s/\tsignal: //" -e "s/\tSSID: //" -e "s/BSS //" -e "s/associated//" -e "s/ -- //" | awk '{ORS = (NR % 3 == 0)? "\n" : " "; print}' | sort`. Try it on a terminal!

    There is not a package for this command. The script runs it directly, stores the output on a temporary file and then retrieves the content of the file.

4. Build a dictionary with the results.
5. Serialize the dictionary to a json string and saves it to a file.

## Run

From the terminal, run `python3 src/run.py some_identifier`
