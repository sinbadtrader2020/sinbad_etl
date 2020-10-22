from src.dbconn.dbclass.company import Company, CompanyConfig
from src.dbconn.dbclassname import DBClassName
from src.dbconn.query import create_or_update_record
from src.remote.company_list_datahub import CompanyListDatahub
from src.remote.company_list_nasdaq import CompanyListNasdaq


class CompanyLoader:
    def __init__(self, config):
        """

        :param config: ConfigParser object where already path set
        """
        self.loaders = [
            CompanyListDatahub(config),
            CompanyListNasdaq(config),
        ]

    def load_companies(self):
        # Load companies from Datahub and insert in DB
        for loader in self.loaders:
            companies = loader.load_companies()
            for row in companies:
                company = Company(*row)

                # TODO check result & success
                result, success = create_or_update_record(table_name=DBClassName.COMPANY,
                                                          conflict_field=CompanyConfig.ACT_SYMBOL,
                                                          return_field=CompanyConfig.COMPANY_ID,
                                                          record=company)