from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from src.infrastructure.database.connection import Base
from typing import Optional
from datetime import datetime


class ClientModel(Base):
    """
    Modelo SQLAlchemy para a tabela clients.
    
    Esta é uma implementação de infraestrutura que não deve vazar
    para as camadas superiores (domínio e aplicação).
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    as camadas superiores não dependem desta implementação.
    """
    __tablename__ = 'clients'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=True)
    cpf = Column(String(14), nullable=False)
    address_id = Column(BIGINT, ForeignKey('addresses.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relacionamentos (se necessário)
    # address = relationship("AddressModel", backref="clients", uselist=False)

    def __repr__(self) -> str:
        return f"<ClientModel(id={self.id}, name='{self.name}', email='{self.email}')>"
