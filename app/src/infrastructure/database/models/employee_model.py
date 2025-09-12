"""
EmployeeModel - Infrastructure Layer

Modelo SQLAlchemy para a tabela employees.

Esta é uma implementação de infraestrutura que não deve vazar
para as camadas superiores (domínio e aplicação).

Aplicando o princípio Dependency Inversion Principle (DIP) - 
as camadas superiores não dependem desta implementação.
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from src.infrastructure.database.connection import Base


class EmployeeModel(Base):
    """
    Modelo SQLAlchemy para a tabela employees.
    """
    __tablename__ = 'employees'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    cpf = Column(String(14), nullable=True)
    status = Column(String(50), nullable=True)
    address_id = Column(BIGINT, ForeignKey('addresses.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relacionamento com Address (assumindo que existe um AddressModel)
    # address = relationship("AddressModel", back_populates="employees")

    def __repr__(self) -> str:
        return f"<EmployeeModel(id={self.id}, name='{self.name}', email='{self.email}', status='{self.status}')>"
