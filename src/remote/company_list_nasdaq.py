from configparser import ConfigParser

from src.remote.company_list_interface import CompanyListInterface
from src.utils.csv_reader import load_csv_data_from_directory
from src.utils import logger


class CompanyListNasdaq(CompanyListInterface):
    """Extract data from a Remote CSV."""

    def __init__(self, config: ConfigParser):
        super().__init__(config)

        self.directory_path = config.get('NASDAQ', 'DIRECTORY')

        logger.info('NASDAQ --> ' +
                    '\n\tDIRECTORY: ' + self.directory_path)

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
        return companies

    def read_companies(self) -> []:
        return self.load_companies()
