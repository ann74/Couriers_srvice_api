from sqlalchemy import Column, Integer, BigInteger, String, ARRAY, Enum
from sqlalchemy.orm import relationship

from app.courier.schemas import CourierType
from app.database.database import Base


class Courier(Base):
    __tablename__ = "courier"

    courier_id = Column(BigInteger, primary_key=True)
    courier_type = Column(Enum(CourierType), nullable=False)
    regions = Column(ARRAY(Integer), nullable=False)
    working_hours = Column(ARRAY(String), nullable=False)

    group_orders = relationship("GroupOrders", back_populates="courier")
