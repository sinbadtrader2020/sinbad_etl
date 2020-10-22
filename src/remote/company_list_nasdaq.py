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

        self.url_registerred_companies = config.get('NASDAQ', 'COMPANIES').split('\n')
        self.tmp_directory = config.get('NASDAQ', 'TEMP_DIRECTORY')
        print('\'NASDAQ\' --> ', self.url_registerred_companies, '\n\r', self.tmp_directory)

        tmp_dir = os.path.join(self.tmp_directory)
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.mkdir(tmp_dir)

    def load_companies(self) -> iter:

        field_names = (
            "Symbol",
            "Name",
            # "LastSale",
            # "MarketCap",
            # "IPOyear",
            # "Sector",
            # "industry",
            # "Summary Quote",
        )

        # Source : https://stackoverflow.com/questions/62686811/getting-time-out-errors-when-downloading-csvs-using-request-api
        headers = {
            'authority': 'www.nasdaq.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
        }

        count = 0
        for path in self.url_registerred_companies:

            req = requests.Request('GET', path, headers=headers)

            prepared = req.prepare()
            pretty_print_http_request(prepared)

            session = requests.Session()
            response = session.send(prepared)

            if response.status_code == 200:
                with open(self.tmp_directory + "/" + str(count) + ".csv", "w") as out:
                    out.write(response.content.decode('utf-8'))
            else:
                print("[ERROR] ", "Cannot Load from URL: ", path)

            count += 1

        companies = load_csv_data_from_directory(directory_name=self.tmp_directory, csv_header=field_names)
        return companies

    def read_companies(self) -> []:
        return self.load_companies()
