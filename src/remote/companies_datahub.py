from datapackage import Package
from src.remote.companies import CompanyInterface


class CompanyDatahub (CompanyInterface):
    """Extract data from a Remote CSV."""

    def load_companies(self, path: str) -> iter:
        package = Package(path)

        # print list of all resources:
        # print(package.resource_names)

        for resource in package.resources:
            if resource.descriptor['datahub']['type'] == 'derived/csv':
                for row in resource.iter():
                    yield row

    def read_companies(self, path: str) -> []:
        package = Package(path)

        # print list of all resources:
        # print(package.resource_names)

        result = []
        for resource in package.resources:
            if resource.descriptor['datahub']['type'] == 'derived/csv':
                result += resource.read()

        return result