from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    """
    Entidade User do domínio - representa um usuário do sistema.
    
    Esta entidade é independente de frameworks e contém apenas a lógica de negócio.
    Aplicando o princípio Single Responsibility Principle (SRP) do SOLID.
    """
    
    # Roles possíveis para usuários
    ROLE_VENDEDOR = "Vendedor"
    ROLE_ADMINISTRADOR = "Administrador"
    
    VALID_ROLES = [ROLE_VENDEDOR, ROLE_ADMINISTRADOR]

    id: Optional[int] = None
    email: str = ""
    password: str = ""  # Hash da senha
    role: str = ""
    employee_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validações após a inicialização"""
        if self.role and not self.is_valid_role(self.role):
            raise ValueError(f"Role inválida. Deve ser uma de: {', '.join(self.VALID_ROLES)}")

    @classmethod
    def create_user(cls, email: str, password_hash: str, role: str, employee_id: Optional[int] = None) -> 'User':
        """
        Método de classe para criar um usuário.
        
        Args:
            email: Email do usuário
            password_hash: Hash da senha
            role: Role do usuário (Vendedor ou Administrador)
            employee_id: ID do funcionário associado (opcional)
            
        Returns:
            User: Nova instância de usuário
            
        Raises:
            ValueError: Se a role for inválida
        """
        if not cls.is_valid_role(role):
            raise ValueError(f"Role inválida. Deve ser uma de: {', '.join(cls.VALID_ROLES)}")
        
        return cls(
            email=email,
            password=password_hash,
            role=role,
            employee_id=employee_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    @classmethod
    def is_valid_role(cls, role: str) -> bool:
        """
        Verifica se a role é válida.
        
        Args:
            role: Role a ser validada
            
        Returns:
            bool: True se a role for válida
        """
        return role in cls.VALID_ROLES

    def is_admin(self) -> bool:
        """
        Verifica se o usuário é administrador.
        
        Returns:
            bool: True se for administrador
        """
        return self.role == self.ROLE_ADMINISTRADOR

    def is_vendedor(self) -> bool:
        """
        Verifica se o usuário é vendedor.
        
        Returns:
            bool: True se for vendedor
        """
        return self.role == self.ROLE_VENDEDOR

    def can_access_admin_features(self) -> bool:
        """
        Verifica se o usuário pode acessar funcionalidades administrativas.
        
        Returns:
            bool: True se puder acessar funcionalidades administrativas
        """
        return self.is_admin()

    def update_role(self, new_role: str) -> None:
        """
        Atualiza a role do usuário.
        
        Args:
            new_role: Nova role do usuário
            
        Raises:
            ValueError: Se a nova role for inválida
        """
        if not self.is_valid_role(new_role):
            raise ValueError(f"Role inválida. Deve ser uma de: {', '.join(self.VALID_ROLES)}")
        
        self.role = new_role
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
