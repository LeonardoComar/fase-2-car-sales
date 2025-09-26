from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from src.infrastructure.database.connection import Base


class MotorVehicleModel(Base):
    """
    Modelo SQLAlchemy para Motor Vehicle.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência dos dados de veículo motorizado.
    """
    
    __tablename__ = "motor_vehicles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String(100), nullable=False, index=True)
    year = Column(String(50), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    mileage = Column(Integer, nullable=False, index=True)
    fuel_type = Column(String(20), nullable=False, index=True)
    color = Column(String(30), nullable=False)
    city = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="Ativo", index=True)
    additional_description = Column(Text)
    
    # Auditoria
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    car = relationship("CarModel", back_populates="motor_vehicle", uselist=False)
    motorcycle = relationship("MotorcycleModel", back_populates="motor_vehicle", uselist=False)
    
    def __repr__(self):
        return f"<MotorVehicleModel(id={self.id}, model='{self.model}', year={self.year})>"
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            "id": self.id,
            "model": self.model,
            "year": self.year,
            "price": self.price,
            "mileage": self.mileage,
            "fuel_type": self.fuel_type,
            "color": self.color,
            "city": self.city,
            "status": self.status,
            "additional_description": self.additional_description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
