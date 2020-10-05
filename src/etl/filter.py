from src.remote.companies_datahub import CompanyDatahub
from src.dbconn.query import create_or_update_record, get_records_partly
from src.dbconn.dbclassname import DBClassName
from src.dbconn.dbclass.company import Company, CompanyConfig
from src.etl.config import FunctionConfig, CompliantConfig
from src.etl.filter_nc_lookup import FilterLookupCategory
from src.etl.filter_nis import FilterNIS
from src.etl.filter_iatr import FilterIATR
from src.etl.filter_dr import FilterDR
from src.etl.filter_nir import FilterNIR
from src.sharedobj import SharedObject

class TradingProcessor:
    def __init__(self):
        self.url_registerred_companies = SharedObject.APP_Config.COMPANIES

        self.path_lookup_csv = SharedObject.APP_Config.DIRECTORY

        self.url_company_report = SharedObject.APP_Config.REPORT
        self.apikey = SharedObject.APP_Config.KEY  # 'JFG78N1VW11CJSOW'

        self.filters = [
            FilterLookupCategory(self.path_lookup_csv),
            FilterNIS(url_string=self.url_company_report, function=FunctionConfig.INCOME_STATEMENT, apikey=self.apikey),
            FilterIATR(url_string=self.url_company_report, function=FunctionConfig.BALANCE_SHEET, apikey=self.apikey),
            FilterDR(url_string=self.url_company_report, function=FunctionConfig.OVERVIEW, apikey=self.apikey),
            FilterNIR(),
        ]

    def load_companies(self):
        # Load companies from Datahub and insert in DB
        companies = CompanyDatahub().load_companies(path=self.url_registerred_companies)
        for row in companies:
            company = Company(*row)

            # TODO check result & success
            result, success = create_or_update_record(table_name=DBClassName.COMPANY,
                                                      conflict_field=CompanyConfig.ACT_SYMBOL,
                                                      return_field=CompanyConfig.COMPANY_ID,
                                                      record=company)

        iter_row = get_records_partly(table_name=DBClassName.COMPANY)
        for row in iter_row:
            company = Company(**row)

            compliant, nc_reason = None, None
            for filter in self.filters:
                compliant, nc_reason = filter(company)
                if compliant != CompliantConfig.COMPLIANT:
                    print('[INFO] ' + nc_reason)
                    break

            company.sf_aaoifi_compliant = compliant
            company.sf_nc_reason = nc_reason

            # TODO check result & success
            result, success = create_or_update_record(table_name=DBClassName.COMPANY,
                                                      conflict_field=CompanyConfig.ACT_SYMBOL,
                                                      return_field=CompanyConfig.COMPANY_ID,
                                                      record=company)
