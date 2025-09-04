from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Date, DateTime, Numeric, ForeignKey, UUID as SqlUUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

if TYPE_CHECKING:
    # Evita imports circulares
    pass


class EmployeeModel(Base):
    """
    Modelo SQLAlchemy para funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela representação da tabela de funcionários.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    pode ser estendido sem modificar código existente.
    """
    
    __tablename__ = "employees"
    
    # Identificação
    id = Column(SqlUUID(as_uuid=True), primary_key=True, index=True)
    employee_id = Column(String(20), unique=True, nullable=False, index=True, 
                        comment="ID interno único do funcionário")
    
    # Dados pessoais
    name = Column(String(255), nullable=False, index=True,
                 comment="Nome completo do funcionário")
    email = Column(String(255), unique=True, nullable=False, index=True,
                  comment="Email corporativo único")
    phone = Column(String(20), nullable=False,
                  comment="Telefone de contato")
    cpf = Column(String(14), unique=True, nullable=False, index=True,
                comment="CPF único do funcionário")
    birth_date = Column(Date, nullable=False,
                       comment="Data de nascimento")
    
    # Dados profissionais
    position = Column(String(100), nullable=False, index=True,
                     comment="Cargo/posição do funcionário")
    department = Column(String(100), nullable=False, index=True,
                       comment="Departamento do funcionário")
    salary = Column(Numeric(10, 2), nullable=False,
                   comment="Salário atual em reais")
    hire_date = Column(Date, nullable=False, index=True,
                      comment="Data de contratação")
    
    # Hierarquia
    manager_id = Column(SqlUUID(as_uuid=True), ForeignKey("employees.id"), nullable=True, index=True,
                       comment="ID do gerente direto")
    manager = relationship("EmployeeModel", remote_side="EmployeeModel.id", back_populates="subordinates")
    subordinates = relationship("EmployeeModel", back_populates="manager")
    
    # Endereço
    address = Column(String(255), nullable=False,
                    comment="Endereço residencial completo")
    city = Column(String(100), nullable=False, index=True,
                 comment="Cidade de residência")
    state = Column(String(2), nullable=False, index=True,
                  comment="Estado (UF) de residência")
    zip_code = Column(String(10), nullable=False,
                     comment="CEP do endereço")
    
    # Contatos de emergência
    emergency_contact_name = Column(String(255), nullable=False,
                                   comment="Nome do contato de emergência")
    emergency_contact_phone = Column(String(20), nullable=False,
                                    comment="Telefone do contato de emergência")
    
    # Status e observações
    status = Column(String(20), nullable=False, default="active", index=True,
                   comment="Status do funcionário: active, inactive, terminated, on_leave")
    notes = Column(String(1000), nullable=True,
                  comment="Observações adicionais sobre o funcionário")
    
    # Auditoria
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True,
                       comment="Data/hora de criação do registro")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow,
                       comment="Data/hora da última atualização")
    
    def __repr__(self):
        return f"<EmployeeModel(id={self.id}, name='{self.name}', position='{self.position}', department='{self.department}')>"
    
    def __str__(self):
        return f"{self.name} - {self.position} ({self.department})"
