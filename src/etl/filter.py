from src.remote.companies_datahub import CompanyDatahub
from src.dbconn.query import create_or_update_record
from src.dbconn.dbclass import DBClassName, Company
from src.etl import filter_nc_lookup


class FilterLookupCategory:
    """
    FilterLookupCategory
    """
    def __init__(self):
        self.lookup = filter_nc_lookup.load_nc_lookup_companies_from_directory(
            '/Users/pothik/Repo/miscellaneous/sinbad_finance/sinbad_finance_etl/file/lookup/')

    def __call__(self, company=None):
        print('Print FilterLookupCategory')

        return True


class FilterNIS:
    """
    NIS: Non-compliant income source (NIS)
    """
    def __call__(self, company=None):
        print('Print NIS: Non-compliant income source (NIS)')

        return True


class FilterIATR:
    """
    IATR: Illiquid asset to total asset ratio
    """
    def __call__(self, company=None):
        print('Print IATR: Illiquid asset to total asset ratio')

        return True


class FilterLAMC:
    """
    LAMC: liquid asset to market capitalization ratio
    """
    def __call__(self, company=None):
        print('Print LAMC: liquid asset to market capitalization ratio')

        return True


class FilterDR:
    """
    DR: interest bearing debt to total asset ratio
    """
    def __call__(self, company=None):
        print('Print DR: interest bearing debt to total asset ratio')

        return True


class FilterNIR:
    """
    NIR: Non-compliant investment to total asset ratio
    """
    def __call__(self, company=None):
        print('Print NIR: Non-compliant investment to total asset ratio')

        return True


class TradingProcessor:
    def load_companies(self):
        # companies = CompanyDatahub().load_companies(path='https://datahub.io/core/nyse-other-listings/datapackage.json')
        companies = CompanyDatahub().load_companies(
            path='https://pkgstore.datahub.io/core/nyse-other-listings/7/datapackage.json')

        for row in companies:
            # data = row.split(',')
            # print(csv.reader(row, delimiter=','))
            company = Company(*row)
            filters = [FilterLookupCategory(), FilterNIS(), FilterIATR(), FilterDR(), FilterNIR()]

            for filter in filters:
                complient = filter(company)
                if not complient:
                    break

            result, success = create_or_update_record(table_name=DBClassName.COMPANY,
                                                      conflict_field='sf_act_symbol',
                                                      return_field='sf_company_id',
                                                      record=company)
            # print(row)

            # print("\n\n")
            # print(CompanyDatahub().load_companies(path='https://datahub.io/core/nyse-other-listings/datapackage.json'))
            #
            # print("\n\n")
            # print(CompanyDatahub().read_companies(path='https://datahub.io/core/nyse-other-listings/datapackage.json'))
