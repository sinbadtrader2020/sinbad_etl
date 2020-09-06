import abc

class CompanyInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_companies') and
                callable(subclass.load_companies) and
                hasattr(subclass, 'read_companies') and
                callable(subclass.read_companies) or
                NotImplemented)

    @abc.abstractmethod
    def load_companies(self, path: str) -> iter:
        """
        Yields the lines of the csv file one by one.
        :param path: Path/ Url of csv file to read.
        :type fn: str
        :rtype: iter
        """
        raise NotImplementedError

    @abc.abstractmethod
    def read_companies(self, path: str) -> []:
        """
        Reads the lines of the csv file at once.
        :param path: Path/ Url of csv file to read.
        :type fn: str
        :rtype: [[...], ..., [...]]
        """
        raise NotImplementedError