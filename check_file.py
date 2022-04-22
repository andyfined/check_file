#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Python script to do a file age check in Icinga2.
License: MIT
"""

from argparse import ArgumentParser
from datetime import datetime
import glob, os

__author__  = 'Andreas Teubner'
__version__ = '1.0.0'
__license__ = 'MIT'

def parse_args():
    parser = ArgumentParser(description='A Python script to do a file age check in Icinga2.')

    parser.add_argument("--file", help="The file to check (regex allowed)", default=None, required=True)
    parser.add_argument("--directory", help="The directory where to check the file", default=None, required=True)
    parser.add_argument("--warning", help="When the state changes to WARNING (in seconds)", default=None)
    parser.add_argument("--critical", help="When the state changes to CRITICAL (in seconds)", default=None)
    parser.add_argument("--version", action="version", version=__version__, help="Show version number")

    return parser.parse_args()

def get_file(file_directory, file_name):
    output_glob = glob.glob(f'{file_directory}{file_name}')
    output_sorted = sorted(output_glob, reverse=True)
    file =  output_sorted[0]

    return file

def get_file_age(file):
    format = '%Y-%m-%d %H:%M:%S'
    real_time = datetime.now().strftime(format)
    file_time = datetime.fromtimestamp(os.path.getmtime(f"{file}")).strftime(format)
    difference = int(round(abs((datetime.strptime(real_time, format) - datetime.strptime(file_time, format)).total_seconds())))

    return difference

def get_state(warn, crit, age, file):
    if age < warn:
        print(f'OK - {file} is {age} seconds old')
        exit(0)
    elif age >= warn and age < crit:
        print(f'WARNING - {file} is {age} seconds old')
        exit(1)
    elif age >= crit:
        print(f'CRITICAL - {file} is {age} seconds old')
        exit(2)

def main(args):
    file_name = ""
    file_directory = ""
    file_warning = 300
    file_critical = 600
    file_full_path = ""
    file_age = 0

    if args.file != None:
        file_name = args.file

    if args.directory != None:
        file_directory = args.directory

    if args.warning != None:
        file_warning = int(args.warning)

    if args.critical != None:
        file_critical = int(args.critical)

    file_full_path = get_file(file_directory,file_name)
    file_age = get_file_age(file_full_path)

    get_state(file_warning, file_critical, file_age, file_full_path)

if __name__ == "__main__":
    args = parse_args()
    main(args)
