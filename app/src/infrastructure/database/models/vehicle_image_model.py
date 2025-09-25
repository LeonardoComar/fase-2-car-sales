"""
VehicleImageModel - Infrastructure Layer

Modelo SQLAlchemy para a tabela vehicle_images.

Esta é uma implementação de infraestrutura que não deve vazar
para as camadas superiores (domínio e aplicação).

Aplicando o princípio Dependency Inversion Principle (DIP) - 
as camadas superiores não dependem desta implementação.
"""

from sqlalchemy import Column, String, INTEGER, BOOLEAN, TIMESTAMP, func, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from src.infrastructure.database.connection import Base
from typing import Optional
from datetime import datetime


class VehicleImageModel(Base):
    """
    Modelo SQLAlchemy para a tabela vehicle_images.
    """
    __tablename__ = 'vehicle_images'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    vehicle_id = Column(BIGINT, ForeignKey('motor_vehicles.id', ondelete='CASCADE'), nullable=False)
    filename = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)
    thumbnail_path = Column(String(500), nullable=True)
    position = Column(INTEGER, nullable=False)
    is_primary = Column(BOOLEAN, nullable=False, default=False)
    uploaded_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    # Relacionamentos (opcional, para consultas)
    # vehicle = relationship("MotorVehicleModel", foreign_keys=[vehicle_id])

    def __repr__(self):
        return f"<VehicleImageModel(id={self.id}, vehicle_id={self.vehicle_id}, filename='{self.filename}', position={self.position})>"
