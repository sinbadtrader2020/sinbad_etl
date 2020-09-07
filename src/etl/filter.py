from src.remote.companies_datahub import CompanyDatahub
from src.dbconn.query import create_or_update_record
from src.dbconn.dbclass import DBClassName, Company
from src.etl.filter_nc_lookup import FilterLookupCategory
from src.etl.filter_nis import FilterNIS


class FilterIATR:
    """
    IATR: Illiquid asset to total asset ratio
    """
    def __call__(self, company=None):
        # print('Print IATR: Illiquid asset to total asset ratio')

        return True


class FilterLAMC:
    """
    LAMC: liquid asset to market capitalization ratio
    """
    def __call__(self, company=None):
        # print('Print LAMC: liquid asset to market capitalization ratio')

        return True


class FilterDR:
    """
    DR: interest bearing debt to total asset ratio
    """
    def __call__(self, company=None):
        # print('Print DR: interest bearing debt to total asset ratio')

        return True


class FilterNIR:
    """
    NIR: Non-compliant investment to total asset ratio
    """
    def __call__(self, company=None):
        # print('Print NIR: Non-compliant investment to total asset ratio')

        return True


class TradingProcessor:
    def load_companies(self):
        # companies = CompanyDatahub().load_companies(path='https://datahub.io/core/nyse-other-listings/datapackage.json')
        companies = CompanyDatahub().load_companies(
            path='https://pkgstore.datahub.io/core/nyse-other-listings/7/datapackage.json')
        filters = [FilterLookupCategory('/Users/pothik/Repo/miscellaneous/sinbad_finance/sinbad_finance_etl/file/lookup/'),
                   FilterNIS(url_string='https://www.alphavantage.co/query',apikey='JFG78N1VW11CJSOW'),
                   FilterIATR(),
                   FilterDR(),
                   FilterNIR()]

        for row in companies:
            # data = row.split(',')
            # print(csv.reader(row, delimiter=','))
            company = Company(*row)

            for filter in filters:
                compliant = filter(company)
                if not compliant:
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
