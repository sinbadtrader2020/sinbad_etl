import os
import shutil
from configparser import ConfigParser

import requests

from src.remote.company_list_interface import CompanyListInterface
from src.utils.csv_reader import load_csv_data_from_directory


def pretty_print_http_request(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
    print('-----------END-----------')


class CompanyListNasdaq(CompanyListInterface):
    """Extract data from a Remote CSV."""

    def __init__(self, config: ConfigParser):
        super().__init__(config)

        self.directory_path = config.get('NASDAQ', 'DIRECTORY')
        print(self.directory_path)
        # field_names = ('Symbol',
        #                'Name',
        #                'LastSale',
        #                'MarketCap',
        #                'IPOyear',
        #                'Sector',
        #                'industry',
        #                'Summary Quote',)
        # self.directory = load_csv_data_from_directory(directory_name=self.directory_path, csv_header=field_names)

    def load_companies(self) -> iter:
        field_names = (
            'Symbol',
            'Name',
            # 'LastSale',
            # 'MarketCap',
            # 'IPOyear',
            # 'Sector',
            # 'industry',
            # 'Summary Quote',
        )

        companies = load_csv_data_from_directory(directory_name=self.directory_path, csv_header=field_names)
        print(companies)
        return companies

    def read_companies(self) -> []:
        return self.load_companies()
