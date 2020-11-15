from configparser import ConfigParser

from datapackage import Package
from src.remote.company_list_interface import CompanyListInterface
from src.utils import logger


class CompanyListDatahub (CompanyListInterface):
    """Extract data from a Remote CSV."""

    def __init__(self, config: ConfigParser):
        super().__init__(config)

        self.url_registerred_companies = config.get('DATAHUB', 'COMPANIES').split('\n')

        logger.info('DATAHUB --> ' + str(self.url_registerred_companies))

    def load_companies(self) -> iter:
        for path in self.url_registerred_companies:
            package = Package(path)

            for resource in package.resources:
                if resource.descriptor['datahub']['type'] == 'derived/csv':
                    for row in resource.iter():
                        yield row

    def read_companies(self) -> []:
        for path in self.url_registerred_companies:
            package = Package(path)

            result = []
            for resource in package.resources:
                if resource.descriptor['datahub']['type'] == 'derived/csv':
                    result += resource.read()

            return result