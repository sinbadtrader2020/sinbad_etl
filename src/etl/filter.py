from datetime import datetime
import inspect
import time

from src.dbconn.query import update_record, get_records_partly
from src.dbconn.dbclassname import DBClassName
from src.dbconn.dbclass.company import Company, CompanyConfig
from src.etl.config import FunctionConfig, CompliantConfig
from src.etl.filter_nc_lookup import FilterLookupCategory
from src.etl.filter_nis import FilterNIS
from src.etl.filter_iatr import FilterIATR
from src.etl.filter_dr import FilterDR
from src.etl.filter_nir import FilterNIR
from src.utils import logger

class TradingProcessor:
    def __init__(self, config):
        self.path_lookup_csv = config.get('LOOKUP', 'DIRECTORY')
        self.url_company_report = config.get('FILTER', 'REPORT')
        self.apikey = config.get('FILTER', 'KEY')  # 'AOYGBU6J7IN09PCE'
        self.max_check = int(config.get('FILTER', 'MAX_CHECK', fallback = 0))
        self.update_frequency = float(config.get('FILTER', 'UPDATE_FREQUENCY', fallback = 86400))

        self.filters = [
            FilterLookupCategory(self.path_lookup_csv),
            FilterNIS(url_string=self.url_company_report, function=FunctionConfig.INCOME_STATEMENT, apikey=self.apikey),
            FilterIATR(url_string=self.url_company_report, function=FunctionConfig.BALANCE_SHEET, apikey=self.apikey),
            FilterDR(url_string=self.url_company_report, function=FunctionConfig.OVERVIEW, apikey=self.apikey),
            FilterNIR(),
        ]

    def load_companies(self):

        iter_row = get_records_partly(table_name=DBClassName.COMPANY)
        update_check_count = 0
        for row in iter_row:
            company = Company(**row)
            company._sf_company_id = row[CompanyConfig.COMPANY_ID]

            timestamp = datetime.timestamp(company.sf_last_screened)
            time_difference = time.time() - timestamp
            if time_difference < self.update_frequency:
                logger.info("filter-" + inspect.stack()[0][3] +
                            "--> Yet to cross update frequency ({0} - {1})".format(company.sf_act_symbol, company.sf_company_name))
                continue


            compliant, nc_reason = None, None
            for filter in self.filters:
                compliant, nc_reason = filter(company)
                if compliant != CompliantConfig.COMPLIANT:
                    logger.info("filter-" + inspect.stack()[0][3] + " --> " + nc_reason)
                    break

            if self.max_check > 0:
                update_check_count += 1
            else:
                update_check_count = 0

            if update_check_count > self.max_check:
                break

            if compliant == CompliantConfig.NETWORK_ERR:
                continue

            company.sf_aaoifi_compliant = compliant
            company.sf_nc_reason = nc_reason

            # TODO check result & success
            result, success = update_record(table_name=DBClassName.COMPANY,
                                            field_value=company._sf_company_id,
                                            field_name=CompanyConfig.COMPANY_ID,
                                            record=company)
