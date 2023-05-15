from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, ARRAY, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base


class Order(Base):
    __tablename__ = "order"

    order_id = Column(BigInteger, primary_key=True)
    weight = Column(Float, nullable=False)
    regions = Column(Integer, nullable=False)
    delivery_hours = Column(ARRAY(String), nullable=False)
    cost = Column(Integer, nullable=False)
    completed_time = Column(DateTime(timezone=True))

    order_group = relationship("OrderGroup", back_populates="order", lazy='joined')


class GroupOrders(Base):
    __tablename__ = "group_orders"

    group_order_id = Column(BigInteger, primary_key=True)
    courier_id = Column(Integer, ForeignKey("courier.courier_id"), nullable=False)

    orders = relationship("OrderGroup", back_populates="group_orders", lazy='joined')
    # courier = relationship("Courier", back_populates="group_orders", lazy='joined')


class OrderGroup(Base):
    __tablename__ = "order_group"

    order_id = Column(BigInteger, ForeignKey("order.order_id"), primary_key=True)
    group_order_id = Column(Integer, ForeignKey("group_orders.group_order_id"), nullable=False)
    complete = Column(Boolean, default=False, nullable=False)

    order = relationship("Order", back_populates="order_group", lazy='joined')
    group_orders = relationship("GroupOrders", back_populates="orders", lazy='joined')
