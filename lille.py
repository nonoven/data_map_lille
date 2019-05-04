#code provenant d'Openclassrooms Crée un data lake
#! /usr/bin/python3
import os
import sys
from time import sleep
import urllib.request

def main():
    if len(sys.argv) < 2:
        print("Usage: python ./{} <path to data directory>".format(sys.argv[0]))
        return 1

    root_dir = sys.argv[1]

    # Lille
    min_latitude = 50.5461539 #ville de Don (Fr)
    min_longitude = 2.9158784 #ville de Don
    max_latitude = 50.7544691 #sud de Dottignies (Be)
    max_longitude = 3.3039251 #ville de Rumes (Be)
    step = 0.001

    longitude = min_longitude
    while longitude < max_longitude:
        latitude = min_latitude
        while latitude < max_latitude:
            try:
                download(root_dir, longitude, latitude, step)
                latitude += step
            except HttpError as e:
                print(e.message, "sleeping 30s...")
                sleep(30)
                continue
        longitude += step

    return 0


def download(root_dir, longitude, latitude, step):
    path = os.path.join(root_dir, "{},{},{},{}.osm".format(
        longitude, latitude, longitude + step, latitude + step
    ))
    if os.path.exists(path):
        # skip file
        return

    # Download
    url = "http://api.openstreetmap.org/api/0.6/map?bbox={},{},{},{}".format(
        longitude, latitude, longitude + step, latitude + step
    )
    response = urllib.request.urlopen(url)

    # Check response
    if response.code != 200:
        message = "Got {} response".format(response.code)
        raise HttpError(message)

    # Write to file
    with open(path, "w") as f:
        f.write(response.read().decode())
        print(path)


class HttpError(Exception):
    pass


if __name__ == "__main__":
sys.exit(main())
