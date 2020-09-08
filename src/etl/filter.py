from src.remote.companies_datahub import CompanyDatahub
from src.dbconn.query import create_or_update_record
from src.dbconn.dbclass import DBClassName, Company
from src.etl.filter_nc_lookup import FilterLookupCategory
from src.etl.filter_nis import FilterNIS
from src.etl.filter_iatr import FilterIATR
from src.etl.filter_dr import FilterDR
from src.etl.filter_nir import FilterNIR


class TradingProcessor:
    def load_companies(self):
        # companies = CompanyDatahub().load_companies(path='https://datahub.io/core/nyse-other-listings/datapackage.json')
        companies = CompanyDatahub().load_companies(
            path='https://pkgstore.datahub.io/core/nyse-other-listings/7/datapackage.json')
        url = 'https://www.alphavantage.co/query'
        apikey = 'AOYGBU6J7IN09PCE'  # 'JFG78N1VW11CJSOW'
        filters = [
            FilterLookupCategory('/Users/pothik/Repo/miscellaneous/sinbad_finance/sinbad_finance_etl/file/lookup/'),
            FilterNIS(url_string=url, function='INCOME_STATEMENT', apikey=apikey),
            FilterIATR(url_string=url, function='BALANCE_SHEET', apikey=apikey),
            # FilterDR(url_string=url, function='OVERVIEW', apikey=apikey),
            # FilterNIR(url_string=url, function='BALANCE_SHEET', apikey=apikey),
        ]

        for row in companies:
            company = Company(*row)

            for filter in filters:
                compliant, nc_reason = filter(company)
                company.sf_aaoifi_compliant = compliant

                if not compliant:
                    print('[INFO] ' + nc_reason)
                    break

                    # TODO commented for testing purpose
                    result, success = create_or_update_record(table_name=DBClassName.COMPANY,
                                                              conflict_field='sf_act_symbol',
                                                              return_field='sf_company_id',
                                                              record=company)
