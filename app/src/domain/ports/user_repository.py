from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.user import User


class UserRepository(ABC):
    """
    Interface do repositório de usuários no domínio.
    
    Define as operações que devem ser implementadas pela infraestrutura.
    Seguindo o princípio Dependency Inversion Principle (DIP) do SOLID.
    """
    
    @abstractmethod
    async def create_user(self, user: User) -> User:
        """
        Cria um novo usuário no banco de dados.
        
        Args:
            user: Dados do usuário a ser criado
            
        Returns:
            User: O usuário criado com ID gerado
            
        Raises:
            Exception: Se houver erro na criação
        """
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca um usuário pelo ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Optional[User]: O usuário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Busca um usuário pelo email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Optional[User]: O usuário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def get_all_users(self) -> List[User]:
        """
        Busca todos os usuários.
        
        Returns:
            List[User]: Lista de todos os usuários
        """
        pass
    
    @abstractmethod
    async def update_user(self, user_id: int, user: User) -> Optional[User]:
        """
        Atualiza um usuário existente.
        
        Args:
            user_id: ID do usuário
            user: Dados atualizados do usuário
            
        Returns:
            Optional[User]: O usuário atualizado ou None se não encontrado
        """
        pass
    
    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        """
        Remove um usuário do banco de dados.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        pass

    @abstractmethod
    async def user_exists_by_email(self, email: str) -> bool:
        """
        Verifica se existe um usuário com o email informado.
        
        Args:
            email: Email a ser verificado
            
        Returns:
            bool: True se existir, False caso contrário
        """
        pass
