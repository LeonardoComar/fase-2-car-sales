"""
MessageModel - Infrastructure Layer

Modelo SQLAlchemy para a tabela messages.

Esta é uma implementação de infraestrutura que não deve vazar
para as camadas superiores (domínio e aplicação).

Aplicando o princípio Dependency Inversion Principle (DIP) - 
as camadas superiores não dependem desta implementação.
"""

from sqlalchemy import Column, String, TEXT, TIMESTAMP, func, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from src.infrastructure.database.connection import Base
from typing import Optional
from datetime import datetime


class MessageModel(Base):
    """
    Modelo SQLAlchemy para a tabela messages.
    """
    __tablename__ = 'messages'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    responsible_id = Column(BIGINT, ForeignKey('employees.id', ondelete='SET NULL'), nullable=True)
    vehicle_id = Column(BIGINT, ForeignKey('motor_vehicles.id', ondelete='SET NULL'), nullable=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=True)
    message = Column(TEXT, nullable=False)
    status = Column(String(50), nullable=False, default="Pendente")
    service_start_time = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relacionamentos (opcional, para consultas)
    # responsible = relationship("EmployeeModel", foreign_keys=[responsible_id])
    # vehicle = relationship("MotorVehicleModel", foreign_keys=[vehicle_id])

    def __repr__(self):
        return f"<MessageModel(id={self.id}, name='{self.name}', status='{self.status}')>"
