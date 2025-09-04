from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class MotorcycleModel(Base):
    """
    Modelo SQLAlchemy para Motorcycle.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência dos dados específicos de motocicleta.
    """
    
    __tablename__ = "motorcycles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    motor_vehicle_id = Column(Integer, nullable=False, unique=True, index=True)
    motorcycle_type = Column(String(30), nullable=False, index=True)
    cylinder_capacity = Column(Integer, nullable=False, index=True)
    has_abs = Column(Boolean, default=False)
    has_traction_control = Column(Boolean, default=False)
    seat_height = Column(Integer, nullable=True)  # em cm
    dry_weight = Column(Integer, nullable=True)  # em kg
    fuel_capacity = Column(Float, nullable=True)  # em litros
    
    # Auditoria
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<MotorcycleModel(id={self.id}, motor_vehicle_id={self.motor_vehicle_id}, type='{self.motorcycle_type}')>"
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            "id": self.id,
            "motor_vehicle_id": self.motor_vehicle_id,
            "motorcycle_type": self.motorcycle_type,
            "cylinder_capacity": self.cylinder_capacity,
            "has_abs": self.has_abs,
            "has_traction_control": self.has_traction_control,
            "seat_height": self.seat_height,
            "dry_weight": self.dry_weight,
            "fuel_capacity": self.fuel_capacity,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
