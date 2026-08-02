from sqlalchemy import select

from db.models.pricing import Pricing
from db.session import SessionLocal
from db.repositories.base_repository import BaseRepository


class PricingRepository(BaseRepository):

    def get_all(self) -> list[Pricing]:
        query = select(Pricing)

        result = self.db.execute(query)
        return result.scalars().all()

    def get_by_destination(self, destination_city: str) -> list[Pricing]:
        query = (
            select(Pricing)
            .where(Pricing.destination_city.ilike(f"%{destination_city}%"))
        )

        result = self.db.execute(query)
        return result.scalars().all()

db = SessionLocal()
pricing_repository = PricingRepository(db)