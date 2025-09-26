"""
AddressModel - Infrastructure Layer

Modelo SQLAlchemy para a tabela addresses.
Representa a estrutura de dados de endereços no banco de dados.

Aplicando o princípio Single Responsibility Principle (SRP) - 
responsável apenas pela estrutura da tabela addresses.
"""

from sqlalchemy import Column, BIGINT, VARCHAR, TIMESTAMP, func
from src.infrastructure.database.connection import Base


class AddressModel(Base):
    """
    Modelo SQLAlchemy para a tabela addresses.
    
    Representa a estrutura de endereços no banco de dados.
    """
    
    __tablename__ = "addresses"
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    street = Column(VARCHAR(100))
    city = Column(VARCHAR(100))
    state = Column(VARCHAR(100))
    zip_code = Column(VARCHAR(20))
    country = Column(VARCHAR(100))
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self) -> str:
        return f"<AddressModel(id={self.id}, city='{self.city}', state='{self.state}')>"
