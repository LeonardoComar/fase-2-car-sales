from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Client:
    """
    Entidade Client do domínio - representa um cliente do sistema.
    
    Esta entidade é independente de frameworks e contém apenas a lógica de negócio.
    Aplicando o princípio Single Responsibility Principle (SRP) do SOLID.
    """

    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: Optional[str] = None
    cpf: str = ""
    address_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create_client(cls, name: str, email: str, cpf: str, phone: Optional[str] = None, 
                     address_id: Optional[int] = None) -> 'Client':
        """
        Método de classe para criar um cliente.
        
        Args:
            name: Nome do cliente
            email: Email do cliente
            cpf: CPF do cliente
            phone: Telefone do cliente (opcional)
            address_id: ID do endereço associado (opcional)
            
        Returns:
            Client: Nova instância de cliente
            
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
            address_id=address_id
        )

    def update_fields(self, name: Optional[str] = None, email: Optional[str] = None,
                     phone: Optional[str] = None, cpf: Optional[str] = None,
                     address_id: Optional[int] = None):
        """
        Atualiza os campos do cliente.
        
        Args:
            name: Novo nome (opcional)
            email: Novo email (opcional)
            phone: Novo telefone (opcional)
            cpf: Novo CPF (opcional)
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
            
        if address_id is not None:
            self.address_id = address_id

    def __str__(self):
        return f"Client(id={self.id}, name='{self.name}', email='{self.email}')"
