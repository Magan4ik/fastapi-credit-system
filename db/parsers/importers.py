from .readers import CSVReader
from api.schemas.models_dto import UserDTO, CreditDTO, PlanDTO, PaymentDTO, TermDTO
from .parsers import UniversalParser

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class ModelImporter:
    reader = CSVReader(sep=r"	")
    parser_class = UniversalParser

    @classmethod
    async def start(cls, session: AsyncSession, model, filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            parser = cls.parser_class(cls.reader, model)
            objects = parser.parse(file)
            for obj in objects:
                orm_model = obj.to_orm()
                session.add(orm_model)

            print(f"model {model} finished")
