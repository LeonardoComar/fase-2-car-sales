from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Employee:
    """
    Entidade Employee do domínio - representa um funcionário do sistema.
    
    Esta entidade é independente de frameworks e contém apenas a lógica de negócio.
    Aplicando o princípio Single Responsibility Principle (SRP) do SOLID.
    """
    
    # Status possíveis para funcionários
    STATUS_ATIVO = "Ativo"
    STATUS_INATIVO = "Inativo"
    
    VALID_STATUSES = [STATUS_ATIVO, STATUS_INATIVO]

    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: Optional[str] = None
    cpf: str = ""
    status: str = STATUS_ATIVO
    address_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validações após a inicialização"""
        if self.status and not self.is_valid_status(self.status):
            raise ValueError(f"Status inválido. Deve ser um de: {', '.join(self.VALID_STATUSES)}")

    @classmethod
    def create_employee(cls, name: str, email: str, cpf: str, phone: Optional[str] = None, 
                       address_id: Optional[int] = None) -> 'Employee':
        """
        Método de classe para criar um funcionário.
        
        Args:
            name: Nome do funcionário
            email: Email do funcionário
            cpf: CPF do funcionário
            phone: Telefone do funcionário (opcional)
            address_id: ID do endereço associado (opcional)
            
        Returns:
            Employee: Nova instância de funcionário
            
        Raises:
            ValueError: Se algum campo obrigatório estiver vazio
        """
        if not name or not name.strip():
            raise ValueError("Nome é obrigatório")
        if not email or not email.strip():
            raise ValueError("Email é obrigatório")
        if not cpf or not cpf.strip():
            raise ValueError("CPF é obrigatório")
            
        return cls(
            name=name.strip(),
            email=email.strip().lower(),
            cpf=cpf.strip(),
            phone=phone.strip() if phone else None,
            address_id=address_id,
            status=cls.STATUS_ATIVO
        )

    @classmethod
    def is_valid_status(cls, status: str) -> bool:
        """Verifica se o status é válido"""
        return status in cls.VALID_STATUSES

    def update_fields(self, name: Optional[str] = None, email: Optional[str] = None,
                     phone: Optional[str] = None, cpf: Optional[str] = None,
                     status: Optional[str] = None, address_id: Optional[int] = None):
        """
        Atualiza os campos do funcionário.
        
        Args:
            name: Novo nome (opcional)
            email: Novo email (opcional)
            phone: Novo telefone (opcional)
            cpf: Novo CPF (opcional)
            status: Novo status (opcional)
            address_id: Novo ID do endereço (opcional)
            
        Raises:
            ValueError: Se algum valor for inválido
        """
        if name is not None:
            if not name.strip():
                raise ValueError("Nome não pode estar vazio")
            self.name = name.strip()
            
        if email is not None:
            if not email.strip():
                raise ValueError("Email não pode estar vazio")
            self.email = email.strip().lower()
            
        if phone is not None:
            self.phone = phone.strip() if phone.strip() else None
            
        if cpf is not None:
            if not cpf.strip():
                raise ValueError("CPF não pode estar vazio")
            self.cpf = cpf.strip()
            
        if status is not None:
            if not self.is_valid_status(status):
                raise ValueError(f"Status inválido. Deve ser um de: {', '.join(self.VALID_STATUSES)}")
            self.status = status
            
        if address_id is not None:
            self.address_id = address_id

    def activate(self):
        """Ativa o funcionário"""
        self.status = self.STATUS_ATIVO

    def deactivate(self):
        """Desativa o funcionário"""
        self.status = self.STATUS_INATIVO

    def is_active(self) -> bool:
        """Verifica se o funcionário está ativo"""
        return self.status == self.STATUS_ATIVO

    def __str__(self):
        return f"Employee(id={self.id}, name='{self.name}', email='{self.email}', status='{self.status}')"
