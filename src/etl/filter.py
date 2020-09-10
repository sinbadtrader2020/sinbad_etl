from src.remote.companies_datahub import CompanyDatahub
from src.dbconn.query import create_or_update_record, get_records_partly
from src.dbconn.dbclass import DBClassName, Company
from src.etl.filter_nc_lookup import FilterLookupCategory
from src.etl.filter_nis import FilterNIS
from src.etl.filter_iatr import FilterIATR
from src.etl.filter_dr import FilterDR
from src.etl.filter_nir import FilterNIR


class TradingProcessor:
    def __init__(self):
        # self.url_registerred_companies = 'https://datahub.io/core/nyse-other-listings/datapackage.json'
        self.url_registerred_companies = 'https://pkgstore.datahub.io/core/nyse-other-listings/7/datapackage.json'

        self.path_lookup_csv = '/Users/pothik/Repo/miscellaneous/sinbad_finance/sinbad_finance_etl/file/lookup/'

        self.url_company_report = 'https://www.alphavantage.co/query'
        self.apikey = 'AOYGBU6J7IN09PCE'  # 'JFG78N1VW11CJSOW'

        self.filters = [
            FilterLookupCategory(self.path_lookup_csv),
            FilterNIS(url_string=self.url_company_report, function='INCOME_STATEMENT', apikey=self.apikey),
            FilterIATR(url_string=self.url_company_report, function='BALANCE_SHEET', apikey=self.apikey),
            FilterDR(url_string=self.url_company_report, function='OVERVIEW', apikey=self.apikey),
            FilterNIR(),
        ]

    def load_companies(self):
        # Load companies from Datahub and insert in DB
        companies = CompanyDatahub().load_companies(path=self.url_registerred_companies)
        for row in companies:
            company = Company(*row)

            # TODO check result & success
            result, success = create_or_update_record(table_name=DBClassName.COMPANY,
                                                      conflict_field='sf_act_symbol',
                                                      return_field='sf_company_id',
                                                      record=company)

        iter_row = get_records_partly(table_name=DBClassName.COMPANY)
        for row in iter_row:
            company = Company(**row)

            compliant, nc_reason = None, None
            for filter in self.filters:
                compliant, nc_reason = filter(company)
                if not compliant:
                    print('[INFO] ' + nc_reason)
                    break

            company.sf_aaoifi_compliant = compliant
            company.sf_nc_reason = nc_reason

            # TODO check result & success
            result, success = create_or_update_record(table_name=DBClassName.COMPANY,
                                                      conflict_field='sf_act_symbol',
                                                      return_field='sf_company_id',
                                                      record=company)
