from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from src.infrastructure.database.connection import Base
from typing import Optional
from datetime import datetime


class UserModel(Base):
    """
    Modelo SQLAlchemy para a tabela users.
    
    Esta é uma implementação de infraestrutura que não deve vazar
    para as camadas superiores (domínio e aplicação).
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    as camadas superiores não dependem desta implementação.
    """
    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)  # Hash da senha
    role = Column(String(50), nullable=False)
    employee_id = Column(BIGINT, ForeignKey('employees.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relacionamentos (se necessário)
    # employee = relationship("EmployeeModel", backref="user", uselist=False)

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, email='{self.email}', role='{self.role}')>"
