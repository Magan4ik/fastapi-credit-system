import datetime
from abc import ABC, abstractmethod
from typing import Type
import re

import pandas as pd
from pandas import DataFrame
from pydantic import BaseModel

from .readers import AbstractReader


class AbstractParser(ABC):

    def __init__(self, reader: AbstractReader):
        self.reader = reader

    @abstractmethod
    def parse(self, file) -> list[BaseModel]:
        pass


class UniversalParser(AbstractParser):

    def __init__(self, reader: AbstractReader, dto_model: Type[BaseModel]):
        super().__init__(reader)
        self.model = dto_model

    def parse(self, file) -> list[BaseModel]:
        df = self.reader.read(file)
        df = self.validate_dataframe(df)

        dtos = list()
        for record in df.to_dict(orient="records"):
            dto = self.model(**record)
            dtos.append(dto)

        return dtos

    def validate_dataframe(self, df: DataFrame) -> DataFrame:
        for col in df.columns:
            if col == "id": continue

            assert col in self.model.model_fields, f"Unexpected field: {col}"

            series = df[col].dropna().astype('str')

            if not series.empty:
                sample = series.iloc[0].strip()
                if re.match(r"^\d{2}\.\d{2}\.\d{4}$", sample):
                    df[col] = pd.to_datetime(df[col], format="%d.%m.%Y").dt.date

        df = df.replace({pd.NA: None}).replace({float('nan'): None})
        return df


if __name__ == "__main__":
    from readers import CSVReader
    from api.schemas import UserDTO, CreditDTO, PlanDTO, PaymentDTO, TermDTO

    parse_mf = {
        UserDTO: "test_dataset/users.csv",
        CreditDTO: "test_dataset/credits.csv",
        PlanDTO: "test_dataset/plans.csv",
        PaymentDTO: "test_dataset/payments.csv",
        TermDTO: "test_dataset/dictionary.csv",
    }

    for model, filename in parse_mf.items():

        file = open(filename, "r", encoding='utf-8')
        csv_reader = CSVReader(sep=r"	")
        parser = UniversalParser(csv_reader, dto_model=model)
        dtos = parser.parse(file)
        print(model, dtos[-1])
