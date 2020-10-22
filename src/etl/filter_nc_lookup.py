from src.etl import common
from src.etl.config import CompliantConfig
from src.utils.csv_reader import load_csv_data_from_directory


class FilterLookupCategory:
    """
    FilterLookupCategory
    """

    def __init__(self, folder_name=None):
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
        self.lookup = load_csv_data_from_directory(directory_name=folder_name, csv_header=field_names)

    def __call__(self, company=None):
        """

        :param company: Company object
        :return: (bool, str)
        """

        for nc_company in self.lookup:
            if company.sf_act_symbol == nc_company['Ticker']:
                return CompliantConfig.NONCOMPLIANT, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.NCL)

        return CompliantConfig.COMPLIANT, common.CMP_CODE
