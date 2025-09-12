"""
SaleModel - Infrastructure Layer

Modelo SQLAlchemy para a tabela sales.

Esta é uma implementação de infraestrutura que não deve vazar
para as camadas superiores (domínio e aplicação).

Aplicando o princípio Dependency Inversion Principle (DIP) - 
as camadas superiores não dependem desta implementação.
"""

from sqlalchemy import Column, Integer, String, DECIMAL, DATE, TEXT, TIMESTAMP, func, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from src.infrastructure.database.connection import Base
from typing import Optional
from decimal import Decimal
from datetime import date


class SaleModel(Base):
    """
    Modelo SQLAlchemy para a tabela sales.
    """
    __tablename__ = 'sales'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    client_id = Column(BIGINT, ForeignKey('clients.id', ondelete='RESTRICT'), nullable=False)
    employee_id = Column(BIGINT, ForeignKey('employees.id', ondelete='RESTRICT'), nullable=False)
    vehicle_id = Column(BIGINT, ForeignKey('motor_vehicles.id', ondelete='RESTRICT'), nullable=False)
    total_amount = Column(DECIMAL(12, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="Pendente")
    sale_date = Column(DATE, nullable=False)
    notes = Column(TEXT, nullable=True)
    discount_amount = Column(DECIMAL(10, 2), nullable=False, default=Decimal('0.00'))
    tax_amount = Column(DECIMAL(10, 2), nullable=False, default=Decimal('0.00'))
    commission_rate = Column(DECIMAL(5, 2), nullable=False, default=Decimal('0.00'))
    commission_amount = Column(DECIMAL(10, 2), nullable=False, default=Decimal('0.00'))
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self) -> str:
        return f"<SaleModel(id={self.id}, client_id={self.client_id}, total={self.total_amount}, status='{self.status}')>"
