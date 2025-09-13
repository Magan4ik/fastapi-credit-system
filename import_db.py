from sqlalchemy.exc import SQLAlchemyError

from db.parsers.importers import ModelImporter

from db.database import async_session
import asyncio
from api.schemas import UserDTO, CreditDTO, PlanDTO, PaymentDTO, TermDTO


async def main():
    models_data = {
        TermDTO: "db/parsers/test_dataset/dictionary.csv",
        UserDTO: "db/parsers/test_dataset/users.csv",
        CreditDTO: "db/parsers/test_dataset/credits.csv",
        PlanDTO: "db/parsers/test_dataset/plans.csv",
        PaymentDTO: "db/parsers/test_dataset/payments.csv",
    }
    async with async_session() as session:
        try:
            async with session.begin():
                for model, filename in models_data.items():
                    await ModelImporter.start(session, model, filename)
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


asyncio.run(main())
