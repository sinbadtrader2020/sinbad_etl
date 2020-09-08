import csv
import os
from csvvalidator import *
import sys
from src.etl import common


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


def load_nc_lookup_companies_from_file(file_name=None):
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
            dict_list.append(line)

    return dict_list


def load_nc_lookup_companies_from_directory(directory_name=None):
    dict_list = []
    with os.scandir(directory_name) as entries:
        for entry in entries:
            tmp = load_nc_lookup_companies_from_file(directory_name + entry.name)
            dict_list.extend(tmp)

    import pprint
    pprint.pprint(dict_list)

    return dict_list


class FilterLookupCategory:
    """
    FilterLookupCategory
    """

    def __init__(self, folder_name=None):
        self.lookup = load_nc_lookup_companies_from_directory(folder_name)

    def __call__(self, company=None):
        """

        :param company: Company object
        :return: (bool, str)
        """

        for nc_company in self.lookup:
            if company.sf_act_symbol == nc_company['Ticker']:
                return False, common.get_nc_reason_string(common.NonCompliantReasonCode.NCL)

        return True, common.CMP_CODE
