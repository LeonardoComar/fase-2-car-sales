"""
Implementação Mock do UserRepository - Infrastructure Layer

Simula operações de persistência para usuários em memória.
Útil para testes e desenvolvimento inicial.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela persistência mock de usuários
- OCP: Extensível para novas operações sem modificar existentes
- LSP: Pode substituir qualquer implementação do repositório
- ISP: Implementa interface específica do repositório
- DIP: Implementa abstração definida no domínio
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio

from src.domain.entities.user import User
from src.domain.ports.user_repository import UserRepository


class MockUserRepository(UserRepository):
    """
    Implementação mock do repositório de usuários.
    
    Armazena dados em memória com simulação de operações assíncronas.
    Mantém integridade referencial e regras de negócio.
    """
    
    def __init__(self):
        """Inicializa o repositório com dados em memória."""
        self._users: Dict[int, User] = {}
        self._email_index: Dict[str, int] = {}
        
        # Simular alguns usuários para desenvolvimento
        self._seed_data()
    
    def _seed_data(self):
        """Popula dados iniciais para desenvolvimento."""
        # Importar bcrypt para criar hash da senha real
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        users_data = [
            {
                "email": "admin@carsales.com",
                "password": pwd_context.hash("admin123456"),  # Hash real da senha
                "role": "Administrador",
                "employee_id": None
            },
            {
                "email": "vendedor01@carsales.com", 
                "password": pwd_context.hash("senha123"),
                "role": "Vendedor",
                "employee_id": 1
            },
            {
                "email": "gerente01@carsales.com",
                "password": pwd_context.hash("senha456"), 
                "role": "Administrador",
                "employee_id": 2
            }
        ]
        
        for data in users_data:
            user_id = len(self._users) + 1
            user = User(
                id=user_id,
                email=data["email"],
                password=data["password"],
                role=data["role"],
                employee_id=data["employee_id"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            self._users[user_id] = user
            self._email_index[user.email] = user_id
    
    async def save(self, user: User) -> User:
        """
        Salva um usuário no repositório.
        
        Args:
            user: Usuário a ser salvo
            
        Returns:
            Usuário salvo com timestamps atualizados
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Se não tem ID, gerar novo
        if user.id is None:
            user.id = len(self._users) + 1
            user.created_at = datetime.now()
        
        # Atualizar timestamp
        user.updated_at = datetime.now()
        
        # Salvar
        self._users[user.id] = user
        
        # Atualizar índices
        self._email_index[user.email] = user.id
        
        return user

    async def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca um usuário por ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Usuário encontrado ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        return self._users.get(user_id)
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca um usuário por email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Usuário encontrado ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        user_id = self._email_index.get(email.lower())
        if user_id:
            return self._users.get(user_id)
        
        return None
    
    async def find_all(self) -> List[User]:
        """
        Busca todos os usuários.
        
        Returns:
            Lista de todos os usuários
        """
        await asyncio.sleep(0.01)  # Simular latência
        return list(self._users.values())
    
    async def count_all(self) -> int:
        """
        Conta total de usuários.
        
        Returns:
            Número total de usuários
        """
        await asyncio.sleep(0.01)  # Simular latência
        return len(self._users)
    
    async def delete(self, user_id: int) -> bool:
        """
        Exclui um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se excluído com sucesso
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        if user_id not in self._users:
            return False
        
        user = self._users[user_id]
        
        # Remover dos índices
        if user.email in self._email_index:
            del self._email_index[user.email]
        
        # Remover usuário
        del self._users[user_id]
        
        return True
    
    async def exists(self, user_id: int) -> bool:
        """
        Verifica se um usuário existe.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se existe
        """
        await asyncio.sleep(0.01)  # Simular latência
        return user_id in self._users
    
    async def email_exists(self, email: str) -> bool:
        """
        Verifica se um email já está em uso.
        
        Args:
            email: Email a verificar
            
        Returns:
            True se existe
        """
        await asyncio.sleep(0.01)  # Simular latência
        return email.lower() in self._email_index

    # Métodos da interface UserRepository
    async def create_user(self, user: User) -> User:
        """Cria um novo usuário no banco de dados."""
        return await self.save(user)
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca um usuário pelo ID."""
        return await self.find_by_id(user_id)
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo email."""
        return await self.find_by_email(email)
    
    async def get_all_users(self) -> List[User]:
        """Busca todos os usuários."""
        return await self.find_all()
    
    async def update_user(self, user_id: int, user: User) -> Optional[User]:
        """Atualiza um usuário existente."""
        existing_user = await self.get_user_by_id(user_id)
        if existing_user:
            user.id = existing_user.id  # Manter o ID original
            return await self.save(user)
        return None
    
    async def delete_user(self, user_id: int) -> bool:
        """Remove um usuário do banco de dados."""
        return await self.delete(user_id)
    
    async def user_exists_by_email(self, email: str) -> bool:
        """Verifica se existe um usuário com o email informado."""
        return await self.email_exists(email)