from extract_data_file.data_extracter import DataExtracter
from abc import ABC, abstractmethod

class DataExtracterEnv(DataExtracter, ABC):

    @staticmethod
    @abstractmethod
    def extract(data, env=None):
        pass