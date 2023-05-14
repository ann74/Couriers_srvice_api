from sqlalchemy import Boolean, Column, ForeignKey, Integer, BigInteger, String, Float, DateTime, ARRAY
from sqlalchemy.orm import relationship

from app.database.database import Base


class Order(Base):
    __tablename__ = "order"

    order_id = Column(BigInteger, primary_key=True)
    weight = Column(Float, nullable=False)
    regions = Column(Integer, nullable=False)
    delivery_hours = Column(ARRAY(String), nullable=False)
    cost = Column(Integer, nullable=False)
    completed_time = Column(DateTime)


