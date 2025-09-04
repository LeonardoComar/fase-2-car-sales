from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class SaleModel(Base):
    """
    Modelo SQLAlchemy para Sale.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência dos dados de venda.
    """
    
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False, index=True)
    vehicle_id = Column(Integer, nullable=False, index=True)  # ID do veículo (car ou motorcycle)
    vehicle_type = Column(String(20), nullable=False, index=True)  # "car" ou "motorcycle"
    
    # Dados da venda
    sale_date = Column(Date, nullable=False, index=True)
    sale_price = Column(Numeric(12, 2), nullable=False)
    discount = Column(Numeric(12, 2), default=0.0)
    final_price = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(50), nullable=False, index=True)
    installments = Column(Integer, default=1)
    
    # Status e observações
    status = Column(String(20), nullable=False, default="Pendente", index=True)
    notes = Column(Text)
    
    # Auditoria
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<SaleModel(id={self.id}, client_id={self.client_id}, final_price={self.final_price})>"
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "employee_id": self.employee_id,
            "vehicle_id": self.vehicle_id,
            "vehicle_type": self.vehicle_type,
            "sale_date": self.sale_date,
            "sale_price": self.sale_price,
            "discount": self.discount,
            "final_price": self.final_price,
            "payment_method": self.payment_method,
            "installments": self.installments,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
