from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.infrastructure.database.connection import Base


class MotorcycleModel(Base):
    """
    Modelo SQLAlchemy para Motorcycle.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência dos dados específicos de motocicleta.
    """
    
    __tablename__ = "motorcycles"
    
    vehicle_id = Column(BIGINT, ForeignKey('motor_vehicles.id'), primary_key=True)
    starter = Column(String(50))
    fuel_system = Column(String(50))
    engine_displacement = Column(Integer)
    cooling = Column(String(50))
    style = Column(String(50))
    engine_type = Column(String(50))
    gears = Column(Integer)
    front_rear_brake = Column(String(100))
    
    # Auditoria
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    # Relacionamento com MotorVehicle
    motor_vehicle = relationship("MotorVehicleModel", back_populates="motorcycle")
    
    def __repr__(self):
        return f"<MotorcycleModel(vehicle_id={self.vehicle_id}, style='{self.style}', engine_displacement={self.engine_displacement})>"
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            "vehicle_id": self.vehicle_id,
            "starter": self.starter,
            "fuel_system": self.fuel_system,
            "engine_displacement": self.engine_displacement,
            "cooling": self.cooling,
            "style": self.style,
            "engine_type": self.engine_type,
            "gears": self.gears,
            "front_rear_brake": self.front_rear_brake,
            "updated_at": self.updated_at
        }
