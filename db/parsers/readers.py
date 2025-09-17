from abc import ABC, abstractmethod
import pandas as pd
from pandas.core.frame import DataFrame


class AbstractReader(ABC):

    @abstractmethod
    def read(self, file, *args, **kwargs) -> DataFrame:
        pass


class CSVReader(AbstractReader):

    def __init__(self, sep=None):
        self.sep = sep

    def read(self, file, *args, **kwargs) -> DataFrame:
        return pd.read_csv(file, *args, sep=self.sep, **kwargs)


class ExcelReader(AbstractReader):

    def read(self, file, *args, **kwargs) -> DataFrame:
        return pd.read_excel(file, *args, **kwargs)
