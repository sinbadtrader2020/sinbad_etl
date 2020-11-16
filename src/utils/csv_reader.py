import csv
import os
from collections import OrderedDict

from csvvalidator import *
import sys


# TODO change and make working
def set_static_validator():
    field_names = ('No.',
                   'Ticker',
                   'Company',
                   'Sector',
                   'Industry',
                   'Country',
                   'Market Cap',
                   'P/E',
                   'Price',
                   'Change',
                   'Volume')
    validator = CSVValidator(field_names)
    validator.add_header_check('EX1', 'bad header')

    def decorate(func):
        setattr(func, 'validator', validator)
        return func

    return decorate


@set_static_validator()
def validate_csv_header(data):
    problems = validate_csv_header.validator.validate(data)
    if problems:
        # write_problems(problems, sys.stdout)
        return False

    return True


def load_csv_data_from_file(file_name=None, csv_header=None):
    if not file_name:
        pass  # TODO add business logic

    dict_list = []
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        # TODO validation does not work
        # if not validate_csv_header(reader):
        #     print("[ERROR]", file_name + " --> CSV Header Problem")
        #     return None

        for line in reader:
            dict_list.append(OrderedDict((i, line[i]) for i in csv_header))

    return dict_list


def load_csv_data_from_directory(directory_name=None, csv_header=None):
    dict_list = []
    with os.scandir(directory_name) as entries:
        for entry in entries:
            tmp = load_csv_data_from_file(directory_name + entry.name, csv_header)
            dict_list.extend(tmp)

    return dict_list