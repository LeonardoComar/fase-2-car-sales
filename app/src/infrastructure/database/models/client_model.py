from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.sql import func
from src.infrastructure.database.connection import Base


class ClientModel(Base):
    """
    Modelo SQLAlchemy para Client.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência dos dados de cliente.
    """
    
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True, index=True)
    birth_date = Column(Date, nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(2), nullable=False, index=True)
    zip_code = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, default="Ativo", index=True)
    notes = Column(Text)
    
    # Auditoria
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ClientModel(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "cpf": self.cpf,
            "birth_date": self.birth_date,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
