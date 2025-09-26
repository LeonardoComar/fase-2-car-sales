from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.infrastructure.database.connection import Base


class CarModel(Base):
    """
    Modelo SQLAlchemy para Car.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência dos dados específicos de carro.
    """
    
    __tablename__ = "cars"
    
    vehicle_id = Column(Integer, ForeignKey('motor_vehicles.id'), primary_key=True)
    transmission = Column(String(20), nullable=False, index=True)
    bodywork = Column(String(30), nullable=False, index=True)
    
    # Relacionamento
    motor_vehicle = relationship("MotorVehicleModel", back_populates="car")
    
    # Auditoria
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<CarModel(vehicle_id={self.vehicle_id}, transmission='{self.transmission}')>"
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            "vehicle_id": self.vehicle_id,
            "transmission": self.transmission,
            "bodywork": self.bodywork,
            "updated_at": self.updated_at
        }
