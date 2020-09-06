import csv
import os
from csvvalidator import *
import sys


# def static_vars(**kwargs):
#     def decorate(func):
#         for k in kwargs:
#             setattr(func, k, kwargs[k])
#         return func
#     return decorate
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


def load_nc_lookup_companies_from_file(file_name = None):
    if not file_name:
        pass    # TODO add business logic

    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        if not validate_csv_header(reader):
            print("[ERROR]", file_name + " --> CSV Header Problem")
            return None

        dict_list = []
        for line in reader:
            dict_list.append(line)

    return dict_list


def load_nc_lookup_companies_from_directory(directory_name = None):
    dict_list = []
    with os.scandir(directory_name) as entries:
        for entry in entries:
            tmp = load_nc_lookup_companies_from_file(directory_name+entry.name)
            dict_list.append(tmp)

    # import pprint
    # pprint.pprint(dict_list)