import abc
from configparser import ConfigParser


class CompanyListInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, '__init__') and
                callable(subclass.__init__) and
                hasattr(subclass, 'load_companies') and
                callable(subclass.load_companies) and
                hasattr(subclass, 'read_companies') and
                callable(subclass.read_companies) or
                NotImplemented)


    def __init__(self, config: ConfigParser):
        """

        :param config: ConfigParser object where already path set
        """
        pass

    @abc.abstractmethod
    def load_companies(self) -> iter:
        """
        Yields the lines of the csv file one by one.
        :rtype: iter
        """
        raise NotImplementedError

    @abc.abstractmethod
    def read_companies(self) -> []:
        """
        Reads the lines of the csv file at once.
        :rtype: [[...], ..., [...]]
        """
        raise NotImplementedError